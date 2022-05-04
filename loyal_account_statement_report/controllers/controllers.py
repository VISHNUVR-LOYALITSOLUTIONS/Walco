# -*- coding: utf-8 -*-
# from odoo import http


# class AccountStatementReport(http.Controller):
#     @http.route('/account_statement_report/account_statement_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_statement_report/account_statement_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_statement_report.listing', {
#             'root': '/account_statement_report/account_statement_report',
#             'objects': http.request.env['account_statement_report.account_statement_report'].search([]),
#         })

#     @http.route('/account_statement_report/account_statement_report/objects/<model("account_statement_report.account_statement_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_statement_report.object', {
#             'object': obj
#         })
