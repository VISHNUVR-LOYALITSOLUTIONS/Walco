# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayrollCancel(http.Controller):
#     @http.route('/hr_payroll_cancel/hr_payroll_cancel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_cancel/hr_payroll_cancel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_cancel.listing', {
#             'root': '/hr_payroll_cancel/hr_payroll_cancel',
#             'objects': http.request.env['hr_payroll_cancel.hr_payroll_cancel'].search([]),
#         })

#     @http.route('/hr_payroll_cancel/hr_payroll_cancel/objects/<model("hr_payroll_cancel.hr_payroll_cancel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_cancel.object', {
#             'object': obj
#         })
