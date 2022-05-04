# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,timedelta
import re



class AccountStatementReportWizard(models.TransientModel):
    _name = "account.statement.report.wizard"
    _description = "Account Statement  Report"

    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company.id)
    date_from = fields.Date(string='Date From', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='Date To', required=True, default=fields.Date.context_today)
    filter_account_type = fields.Selection([('payable', 'Payable'), ('receivable', 'Receivable'), ],
                                           string="Account", default='payable')
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    state = fields.Selection([ ('posted', 'All Posted Entries'),('all', 'All Entries')], string="Target Moves",
                             default='posted', required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    allowed_company_ids = fields.Many2many('res.company', string="Allowed company",
                                           compute="compute_context_allowed_company")

    @api.depends('user_id')
    def compute_context_allowed_company(self):
        allowed_companies = self.env['res.company'].browse(self._context.get('allowed_company_ids'))
        self.allowed_company_ids = allowed_companies

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['partner_id'] = data['form']['partner_id'] or False
        result['company_id'] = data['form']['company_id'] or False
        result['selected_company_id'] = data['form']['company_id'] or False
        result['user_id'] = data['form']['user_id'] or False
        ctx = dict(self.env.context)
        ctx = {'selected_company_id': data['form']['company_id'] or False}
        self.env.context = ctx
        result['filter_account_type'] = data['form']['filter_account_type'] or False

        date_from = data['form']['date_from']
        previous_date = date_from - timedelta(days=1)
        result['previous_date'] =previous_date
        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = 'account.move.line'
        data['form'] = self.read()[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        print('data in check_print',data)
        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('loyal_account_statement_report.action_account_statement_report_pdf').report_action(self, data=data)


    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'account.move.line'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('loyal_account_statement_report.action_account_statement_report_xls').report_action(self, data=datas)










