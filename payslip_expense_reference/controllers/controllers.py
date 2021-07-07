# -*- coding: utf-8 -*-
# from odoo import http


# class PayslipExpenseReference(http.Controller):
#     @http.route('/payslip_expense_reference/payslip_expense_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payslip_expense_reference/payslip_expense_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payslip_expense_reference.listing', {
#             'root': '/payslip_expense_reference/payslip_expense_reference',
#             'objects': http.request.env['payslip_expense_reference.payslip_expense_reference'].search([]),
#         })

#     @http.route('/payslip_expense_reference/payslip_expense_reference/objects/<model("payslip_expense_reference.payslip_expense_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payslip_expense_reference.object', {
#             'object': obj
#         })
