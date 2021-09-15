# -*- coding: utf-8 -*-
# from odoo import http


# class HeaderFooterCompany(http.Controller):
#     @http.route('/header_footer_company/header_footer_company/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/header_footer_company/header_footer_company/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('header_footer_company.listing', {
#             'root': '/header_footer_company/header_footer_company',
#             'objects': http.request.env['header_footer_company.header_footer_company'].search([]),
#         })

#     @http.route('/header_footer_company/header_footer_company/objects/<model("header_footer_company.header_footer_company"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('header_footer_company.object', {
#             'object': obj
#         })
