# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields, _
from datetime import datetime,timedelta,date
import re


class AccountStatementReportPDF(models.AbstractModel):
    _name = 'report.loyal_account_statement_report.statement_report_pdf'

    @api.model
    def _query_get(self, data=None):
        domain = [
            ('display_type', 'not in', ('line_section', 'line_note')),
            ('company_id', '=', data['form']['company_id'][0]),
            ('date', '<=', data['form']['date_to']),
            ('date', '>=', data['form']['date_from']),
            ('partner_id', '=', data['form']['partner_id'][0]),
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

        user_company = self.env['res.company'].browse(data['form']['company_id'][0])
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

        # account_move_line__move_id.del_no AS  del_no,
        # account_move_line__move_id.cpo_number  AS cpo_no,

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
            ('company_id', '=', data['form']['company_id'][0]),
            ('date', '<=', fields.Date.to_string(new_date_to)),
            ('partner_id', '=', data['form']['partner_id'][0]),
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

    @api.model
    def _get_report_values(self, docids, data=None):
        partner_id = data['form']['partner_id'][0]
        company_id = data['form']['company_id'][0]
        target_move = data['form']['state']
        account_type = data['form']['filter_account_type']
        company = self.env['res.company'].browse(company_id)
        partner = self.env['res.partner'].browse(partner_id)
        credit_days=""
        if partner.customer_rank>0:
            credit_days = partner.property_payment_term_id.name if partner.property_payment_term_id.name else " "
        else:
            credit_days = partner.property_supplier_payment_term_id.name if partner.property_supplier_payment_term_id.name else " "

        statements = self.get_account_statements(data)
        initial_balance = self.get_initial_balance(data)
        context = {'include_nullified_amount': True}

        sign = -1.0 if self.env.context.get('aged_balance') else 1.0
        lines = []
        account_types = [self.env.context.get('account_type')]
        context = {'include_nullified_amount': True}
        partner_id = self.env['res.partner'].browse(partner_id)

        context.update(partner_ids=partner_id)


        movelines, total, dummy = self.env['report.account.report_agedpartnerbalance'].with_context(**context)._get_partner_move_lines([account_type], data['form']['date_to'],
                                                               target_move,
                                                               30)
        date_from = data['form']['date_from']
        date_from_date = datetime.strptime(date_from, '%Y-%m-%d')
        # entered_date = datetime.datetime.strptime(date_from_date, '%Y-%m-%d')
        # entered_date = entered_date.date()
        entered_date = date_from_date - timedelta(days=1)
        previous_date = entered_date.date()

        docargs = {
            'doc_ids': docids,
            'doc_model': self.env['account.move.line'],
            'data': data,
            'partner': partner,
            'date_from': data['form']['date_from'],
            'date_to': data['form']['date_to'],
            'filter_account_type': data['form']['filter_account_type'],
            'previous_date':previous_date,
            'statements': statements,
            'company': company,
            'bank_details': company,
            'credit_days':credit_days,
            'initial_balance': initial_balance,
            'get_partner_lines': movelines,
            'get_direction': total,
        }
        return docargs

