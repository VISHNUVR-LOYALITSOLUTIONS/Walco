from odoo import api, models, fields, _
from datetime import timedelta, datetime
from odoo.exceptions import UserError
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell



class AccountStatementReportXls(models.AbstractModel):
    _name = 'report.loyal_account_statement_report.statement_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def _query_get(self, data=None):
        domain = [
            ('display_type', 'not in', ('line_section', 'line_note')),
            ('company_id', '=', data['form']['company_id']),
            ('date', '<=', data['form']['date_to']),
            ('date', '>=', data['form']['date_from']),
            ('partner_id', '=', data['form']['partner_id']),
            ('account_id.internal_type', '=', data['form']['filter_account_type'])
        ]
        if data['form']['state'] == 'posted':
            domain.append(('move_id.state', '=', 'posted'))
        else:
            domain.append(('move_id.state', '!=', 'cancel'))
        self.env['account.move.line'].check_access_rights('read')
        query = self.env['account.move.line']._where_calc(domain)

        # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
        self.env['account.move.line']._apply_ir_rules(query)

        return query.get_sql()

    @api.model
    def _get_query_currency_table(self, data):
        ''' Construct the currency table as a mapping company -> rate to convert the amount to the user's company
        currency in a multi-company/multi-currency environment.
        The currency_table is a small postgresql table construct with VALUES.
        :param options: The report options.
        :return:        The query representing the currency table.
        '''

        user_company = self.env['res.company'].browse(data['form']['company_id'])
        user_currency = user_company.currency_id
        companies = user_company
        currency_rates = {user_currency.id: 1.0}

        conversion_rates = []
        for company in companies:
            conversion_rates.append((
                company.id,
                currency_rates[user_company.currency_id.id] / currency_rates[company.currency_id.id],
                user_currency.decimal_places,
            ))

        currency_table = ','.join('(%s, %s, %s)' % args for args in conversion_rates)
        return '(VALUES %s) AS currency_table(company_id, rate, precision)' % currency_table

    def get_account_statements(self, data):

        lines = []
        params = []
        # Create the currency table.
        ct_query = self._get_query_currency_table(data)
        tables, where_clause, where_params = self._query_get(data)
        params += where_params

        query = ('''
                SELECT
                    account_move_line.id,
                    account_move_line__move_id.id AS move_id,
                    account_move_line.date,
                    account_move_line__move_id.name AS invoice_no,
                    partner.name AS partner_name,
                    account_move_line__move_id.invoice_origin AS po_no,
                    account_move_line__move_id.cpo_number AS cpo_no,
                    account_move_line__move_id.cpo_reference AS cpo_reference,
                    payment_term.name as term,
                    account_move_line__move_id.invoice_date AS invoice_date,
                account_move_line__move_id.amount_residual AS amount_residual,
                account_move_line__move_id.invoice_date_due AS due,
                account_move_line__move_id.amount_total AS invoice_amount,
                 CURRENT_DATE-account_move_line__move_id.invoice_date_due as aging_date,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    account_move_line.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    ROUND((CASE WHEN account_move_line.debit is not NULL or FALSE then account_move_line.debit * currency_table.rate ELSE 0 END), currency_table.precision)   AS debit,
                --ROUND(account_move_line.debit * currency_table.rate, currency_table.precision)   AS debit,
                ROUND((CASE WHEN account_move_line.credit is not NULL or FALSE then account_move_line.credit * currency_table.rate ELSE 0 END), currency_table.precision)   AS credit,
                --ROUND(account_move_line.credit * currency_table.rate, currency_table.precision)  AS credit,
                ROUND((CASE WHEN account_move_line.balance is not NULL or FALSE then account_move_line.balance * currency_table.rate ELSE 0 END), currency_table.precision)   AS balance,
                --ROUND(account_move_line.balance * currency_table.rate, currency_table.precision) AS balance,
                    company.currency_id AS company_currency_id,
                    account_move_line__move_id.type AS move_type,
                    account.code AS account_code,
                    account.name AS account_name,
                    journal.code AS journal_code,
                    journal.name AS journal_name,
                    full_rec.name AS full_rec_name
                    FROM account_move_line
                    LEFT JOIN account_move account_move_line__move_id ON account_move_line__move_id.id = account_move_line.move_id
                    LEFT JOIN %s ON currency_table.company_id = account_move_line.company_id
                    LEFT JOIN res_company company               ON company.id = account_move_line.company_id
                    LEFT JOIN res_partner partner               ON partner.id = account_move_line.partner_id
                    LEFT JOIN account_account account           ON account.id = account_move_line.account_id
                    LEFT JOIN account_journal journal           ON journal.id = account_move_line.journal_id
                    LEFT JOIN account_full_reconcile full_rec   ON full_rec.id = account_move_line.full_reconcile_id
                    LEFT JOIN account_payment_term  payment_term ON payment_term.id = account_move_line__move_id.invoice_payment_term_id
                    WHERE %s
                    ORDER BY account_move_line.id'''
                 % (ct_query, where_clause))
        self._cr.execute(query, params)
        for res in self._cr.dictfetchall():
            res['dn_no'] = " "
            if res['move_type'] in ['in_invoice', 'in_refund']:
                po_id = self.env['purchase.order'].search([('name', '=', res['po_no'])])
                dn_no = ', '.join(picking.name for picking in po_id.picking_ids if picking.state != 'cancel')
                res['dn_no'] = dn_no
            if res['move_type'] in ['out_invoice', 'out_refund']:
                po_id = self.env['sale.order'].search([('name', '=', res['po_no'])])
                dn_no = ', '.join(picking.name for picking in po_id.picking_ids if picking.state != 'cancel')
                res['dn_no'] = dn_no
            lines.append(res)
        return lines

    def _initial_balance_query_get(self, data=None):
        new_date_to = fields.Date.from_string(data['form']['date_from']) - timedelta(days=1)
        domain = [
            ('display_type', 'not in', ('line_section', 'line_note')),
            ('company_id', '=', data['form']['company_id']),
            ('date', '<=', fields.Date.to_string(new_date_to)),
            ('partner_id', '=', data['form']['partner_id']),
            ('account_id.internal_type', '=', data['form']['filter_account_type'])
        ]
        if data['form']['state'] == 'posted':
            domain.append(('move_id.state', '=', 'posted'))
        else:
            domain.append(('move_id.state', '!=', 'cancel'))
        self.env['account.move.line'].check_access_rights('read')
        query = self.env['account.move.line']._where_calc(domain)

        # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
        self.env['account.move.line']._apply_ir_rules(query)

        return query.get_sql()

    def get_initial_balance(self, data):
        initial_balance = 0
        params = []
        # Create the currency table.
        ct_query = self._get_query_currency_table(data)
        tables, where_clause, where_params = self._initial_balance_query_get(data)
        params += where_params
        query = ('''SELECT
                account_move_line.partner_id,
                SUM(ROUND(account_move_line.debit * currency_table.rate, currency_table.precision))   AS debit,
                SUM(ROUND(account_move_line.credit * currency_table.rate, currency_table.precision))  AS credit,
                SUM(ROUND(account_move_line.balance * currency_table.rate, currency_table.precision)) AS balance
                FROM account_move_line
                LEFT JOIN account_move account_move_line__move_id ON account_move_line__move_id.id = account_move_line.move_id
                LEFT JOIN %s ON currency_table.company_id = account_move_line.company_id
                WHERE %s
                GROUP BY account_move_line.partner_id '''
                 % (ct_query, where_clause))
        self._cr.execute(query, params)
        for res in self._cr.dictfetchall():
            initial_balance += res['balance']
        return initial_balance

    def generate_xlsx_report(self, workbook, data, lines):

        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        sheet = workbook.add_worksheet(_('Account Statement Report'))
        sheet.set_landscape()
        sheet.set_default_row(25)
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        # sheet.set_column(0, 0, 20)
        # sheet.set_column(1, 1, 20)
        # sheet.set_column(2, 2, 25)
        # sheet.set_column(3, 5, 20)
        # sheet.set_column(4, 5, 20)


        # sheet.set_column(1, 1, 20)
        # sheet.set_column(2, 2, 25)
        # sheet.set_column(3, 3, 25)
        # sheet.set_column(4, 4, 20)
        # sheet.set_column(5, 5, 25)
        # sheet.set_column(6, 6, 20)
        # sheet.set_column(7, 7, 20)
        # sheet.set_column(8, 8, 20)
        # sheet.set_column(9, 9, 20)
        # sheet.set_column(10, 10, 20)
        # sheet.set_column(11, 11, 20)
        # sheet.set_column(12, 12, 20)
        # sheet.set_column(13, 13, 20)
        # sheet.set_column(14, 14, 20)
        # sheet.set_column(15, 15, 20)
        # sheet.set_column(16, 16, 20)
        # sheet.set_column(17, 17, 20)
        # sheet.set_column(18, 18, 20)
        # sheet.set_column(19, 19, 20)
        # sheet.set_column(20, 20, 20)
        # sheet.set_column(21, 21, 30)
        # sheet.set_column(22, 22, 20)
        # sheet.set_column(23, 23, 20)
        # sheet.set_column(24, 24, 20)

        partner_id = data['form']['partner_id']
        company_id = data['form']['company_id']
        company = self.env['res.company'].browse(company_id)
        partner = self.env['res.partner'].browse(partner_id)
        statements = self.get_account_statements(data)
        initial_balance = self.get_initial_balance(data)

        credit_days = ""
        if partner.customer_rank > 0:
            credit_days = partner.property_payment_term_id.name if partner.property_payment_term_id.name else " "
        else:
            credit_days = partner.property_supplier_payment_term_id.name if partner.property_supplier_payment_term_id.name else " "
        net_credit_val =[]
        if credit_days:
            net_credit_val=[int(word) for word in credit_days.split() if word.isnumeric()]


        target_move = data['form']['state']
        account_type = data['form']['filter_account_type']

        context = {'include_nullified_amount': True}

        context = {'include_nullified_amount': True}

        context.update(partner_ids=partner)

        movelines, total_aging, dummy = self.env['report.account.report_agedpartnerbalance'].with_context(
            **context)._get_partner_move_lines([account_type], data['form']['date_to'],
                                               target_move,
                                               30)

        date_start = data['form']['date_from']
        date_end = data['form']['date_to']
        if date_start:
            date_object_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            date_object_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()

        res_balance = 0
        for line in statements:
            if line['balance']:
                res_balance+=line['balance']



        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14})
        font_size_8_center_red = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'center',
             'color': 'red'})
        font_size_8_center_blue = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'center',
             'color': 'blue'})
        font_size_8_center_green = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'center',
             'color': 'green'})
        font_size_8_center_black = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'center',
             'color': 'black'})


        font_size_8_center = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True,'right': True, 'font_size': 12, 'align': 'center','color': '#13076e'})
        font_size_8_right = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'right','color': '#13076e'})
        font_size_8_left = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True,'font_size': 12, 'align': 'left','color': '#13076e'})

        font_size_9_left = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 12, 'align': 'left',
             'color': '#13076e','bold': True})

        bg_font_size_8_right = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True,'right': True, 'font_size': 12, 'align': 'right', 'color': 'black','bg_color': str(company.primary_color),})
        bg_font_size_8_center = workbook.add_format(
            # {'bottom': True, 'top': True, 'left': True,'right': True, 'font_size': 12, 'align': 'center', 'color': 'black','bg_color': '#c1c3dd',})
            {'bottom': True, 'top': True, 'left': True,'right': True, 'font_size': 12, 'align': 'center', 'color': 'black','bg_color': str(company.primary_color),})

        big_font_size_8_center = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'right': True, 'font_size': 14, 'align': 'center',
             'color': 'black', 'bg_color': str(company.primary_color),'bold': True })

        formattotal = workbook.add_format(
            {'bg_color': 'e2e8e8', 'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
             'align': 'right', 'bold': True})


        blue_mark2 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 16, 'bold': True,
             'align': 'left','color': 'black'})
        font_size_8bold = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True, })

        blue_mark3 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 18, 'bold': True,
             'color':'#13076e', 'bg_color': '#ffffff', 'align': 'center'})
        blue_mark8 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 16, 'bold': True,
             'align': 'left','color': '#13076e'})

        blue_mark12 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 16, 'bold': True,
             'align': 'left','color': 'black','bg_color': str(company.primary_color),})
        # bg_color
        ': '  # 808080', 'color': '#FFFFFF',

        title_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': str(company.primary_color), 'color': 'black',
                                           'bottom': 1, 'align': 'center','border':1})
        account_style = workbook.add_format({'font_size': 12, 'bold': True,
                                           'bg_color': str(company.secondary_color), 'color': '#000000',
                                           'bottom': 1, 'align': 'right','border':1})
        sheet.set_column(0,0, 20)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 35)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 30)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)
        sheet.set_column(8, 8, 20)
        sheet.set_column(9, 9, 20)
        sheet.set_column(10, 10, 20)
        sheet.set_column(11, 11, 20)
        sheet.set_column(12, 12, 20)
        sheet.set_column(13, 13, 20)
        sheet.set_column(14, 14, 20)
        sheet.set_column(15, 15, 20)
        sheet.set_column(16, 16, 20)
        sheet.set_column(17, 17, 20)
        sheet.set_column(18, 18, 20)
        sheet.set_column(19, 19, 20)
        sheet.set_column(20, 20, 20)
        sheet.set_column(21, 21, 30)
        sheet.set_column(22, 22, 20)
        sheet.set_column(23, 23, 20)
        sheet.set_column(24, 24, 20)
        # sheet.insert_image('A1', '/account_statement_report/static/description/src/img/page.jpg')
        sheet.insert_image('A1', '/loyal_account_statement_report/static/description/src/img/logo.png')
        # sheet.set_header('&C&G', {'image_center': '/account_statement_report/static/description/src/img/logo.png'})
        sheet.merge_range('A5:H5', 'STATEMENT OF ACCOUNT', blue_mark3)
        # sheet.merge_range('A6:G6', company.name, blue_mark2)
        sheet.write('A7', "Client", blue_mark2)
        # sheet.merge_range('A7', "Client", blue_mark2)
        sheet.merge_range('B7:D7', partner.name, blue_mark8)
        sheet.merge_range('E7:H7', "", blue_mark12)

        sheet.write('A8', "Period", blue_mark2)
        sheet.merge_range('B8:D8', date_object_date_start.strftime(
            '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), blue_mark8)
        # sheet.merge_range('D8', "", blue_mark2)
        sheet.merge_range('E8:F8', "Current Due:", blue_mark12)
        sheet.merge_range('G8:H8', res_balance+initial_balance, blue_mark12)

        # sheet.merge_range('A9', "Credit Days", blue_mark2)
        sheet.write('A9', "Credit Days", blue_mark2)
        sheet.merge_range('B9:D9', credit_days, blue_mark8)
        # sheet.merge_range('D9', "", blue_mark2)
        sheet.merge_range('E9:H9', "", blue_mark12)




        sheet.write('A11', "Invoice Date", title_style)
        sheet.write('B11', "Invoice No.", title_style)
        sheet.write('C11', "Customer Order Reference", title_style)
        sheet.write('D11', "Invoice Amount (SAR)", title_style)
        sheet.write('E11', "Paid Amount (SAR)", title_style)
        sheet.write('F11', "Balance Amount (SAR)", title_style)
        sheet.write('G11', "Aging Days", title_style)
        sheet.write('H11', "Actual Due date", title_style)
        sheet.merge_range('A12:E12', "PREVIOUS BALANCE", account_style)
        sheet.write('F12', '{0:,.2f}'.format(float(initial_balance)) if initial_balance else 0, account_style)
        sheet.write('G12', "", account_style)
        sheet.write('H12', "", account_style)

        debittotal = 0
        credittotal = 0
        balance = 0
        row = 13
        for line in statements:
            sheet.write(row, 0, line['date'].strftime('%d-%b-%Y') if line['date'] else " ", font_size_8_center)
            sheet.write(row, 1, line['invoice_no'] if line['invoice_no'] else " ", font_size_8_center)
            sheet.write(row, 2, line['cpo_reference'] if line['cpo_reference'] else " ", font_size_8_center)
            sheet.write(row, 3, '{0:,.2f}'.format(float(line['debit'])) if line['debit'] else 0, font_size_8_right)
            debittotal = debittotal + line['debit']
            sheet.write(row, 4, '{0:,.2f}'.format(float(line['credit'])) if line['credit'] else 0, font_size_8_right)
            credittotal = credittotal + line['credit']
            sheet.write(row, 5, '{0:,.2f}'.format(float(debittotal-credittotal+initial_balance)) if debittotal-credittotal+initial_balance else 0, font_size_8_right)
            balance = balance + line['balance']
            if net_credit_val:
                if line['aging_date']:
                    if line['aging_date']>net_credit_val[0]:
                        sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center_red)
                    elif line['aging_date']<net_credit_val[0]:
                        sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center_green)
                    elif line['aging_date']==net_credit_val[0]:
                        sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center_black)
                    else:
                        sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center_blue)

            else:
                if line['aging_date']:
                    sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center_blue)

            # sheet.write(row, 6, line['aging_date'] if line['aging_date'] else " ", font_size_8_center)
            sheet.write(row, 7, line['due'].strftime('%d-%b-%Y') if line['due'] else " ", font_size_8_center)

            row += 1

        line_column = 0

        line_column = 0

        sheet.merge_range(row, 0, row, 1, "Grand Total", big_font_size_8_center)

        total_cell_range12 = xl_range(13, 2, row - 1, 2)

        total_cell_range11 = xl_range(13, 3, row - 1, 3)
        total_cell_range = xl_range(13, 4, row - 1, 4)
        # total_cell_range5 = xl_range(8, 5, row - 1, 5)
        total_cell_range6 = xl_range(13, 6, row - 1, 6)
        total_cell_range7 = xl_range(13, 7, row - 1, 7)
        # total_cell_range8 = xl_range(8, 8, row - 1, 8)
        # total_cell_range9 = xl_range(8, 9, row - 1, 9)


        sheet.write_formula(row, 2, '=SUM(' + total_cell_range12 + ')', bg_font_size_8_center)
        sheet.write_formula(row, 3, '=SUM(' + total_cell_range11 + ')', bg_font_size_8_right)
        sheet.write_formula(row, 4, '=SUM(' + total_cell_range + ')', bg_font_size_8_right)
        sheet.write(row, 5, '{0:,.2f}'.format(float(balance + initial_balance)) if balance + initial_balance else 0,  bg_font_size_8_right)
        # sheet.write_formula(row, 5, '=SUM(' + total_cell_range5 + ')', bg_font_size_8_right)
        sheet.write_formula(row, 6, '=SUM(' + total_cell_range6 + ')', bg_font_size_8_right)
        sheet.write_formula(row, 7, '=SUM(' + total_cell_range7 + ')', bg_font_size_8_center)
        # sheet.write_formula(row, 8, '=SUM(' + total_cell_range8 + ')', font_size_8_center)
        # sheet.write_formula(row, 9, '=SUM(' + total_cell_range9 + ')', font_size_8_center)

        # row += 3
        #
        #
        # sheet.write(row, line_column, "Aging Days", title_style)
        # sheet.write(row, line_column+1, "Amount", title_style)
        # row+=1
        # if total_aging:
        #     sheet.write(row, line_column, "1 - 30 Days", font_size_8_left)
        #     sheet.write(row, line_column + 1, total_aging[4], font_size_8_right)
        #     row += 1
        #     sheet.write(row, line_column, "31 - 60 days", font_size_8_left)
        #     sheet.write(row, line_column + 1, total_aging[3], font_size_8_right)
        #     row += 1
        #     sheet.write(row, line_column, "61 - 90 Days", font_size_8_left)
        #     sheet.write(row, line_column + 1, total_aging[2], font_size_8_right)
        #     row += 1
        #     sheet.write(row, line_column, "91 - 120 Days", font_size_8_left)
        #     sheet.write(row, line_column + 1, total_aging[1], font_size_8_right)
        #     row += 1
        #     sheet.write(row, line_column, "120- Above", font_size_8_left)
        #     sheet.write(row, line_column + 1, total_aging[0], font_size_8_right)

        row += 5


        sheet.merge_range(row, 0, row, 2, "Accounts Dept._______________________", font_size_9_left)
        sheet.merge_range(row, 5, row, 7, "Finance Dept.._______________________", font_size_9_left)



        # sheet.write(row, 1, "Bank Name", title_style)
        # sheet.write(row, 2, "Account No.", title_style)
        # sheet.write(row, 3, "IBAN No.", title_style)

        row += 3

        sheet.merge_range(row,0,row,2, "Bank Name", title_style)
        sheet.merge_range(row,3,row, 4, "Account No.", title_style)
        sheet.merge_range(row,5,row, 7, "IBAN No.", title_style)

        row+=1

        for line in company.partner_id.bank_ids:
            sheet.merge_range(row,0,row,1,line.bank_id.name if line.bank_id.name else " ", font_size_8_left)
            sheet.write(row, 2, line.bank_id.name_arabic if line.bank_id.name_arabic else " ", font_size_8_right)
            sheet.merge_range(row,3,row, 4, line.acc_number if line.acc_number else " ", font_size_8_center)
            sheet.merge_range(row,5,row, 7, line.bank_id.bic if line.bank_id.bic else " ", font_size_8_center)

            row += 1







        #
        # sheet.merge_range(row, 0, row, 8, "ACCOUNT CURRENT BALANCE", account_style)
        # sheet.write(row, 9, balance+initial_balance, account_style)

