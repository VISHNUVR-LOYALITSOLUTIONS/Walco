# -*- coding: utf-8 -*-
# from odoo import http


# class CompanyReportTemplate(http.Controller):
#     @http.route('/company_report_template/company_report_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_report_template/company_report_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_report_template.listing', {
#             'root': '/company_report_template/company_report_template',
#             'objects': http.request.env['company_report_template.company_report_template'].search([]),
#         })

#     @http.route('/company_report_template/company_report_template/objects/<model("company_report_template.company_report_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_report_template.object', {
#             'object': obj
#         })
