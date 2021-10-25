# -*- coding: utf-8 -*-
# from odoo import http


# class SqccInvoicePrint(http.Controller):
#     @http.route('/sqcc_invoice_print/sqcc_invoice_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sqcc_invoice_print/sqcc_invoice_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sqcc_invoice_print.listing', {
#             'root': '/sqcc_invoice_print/sqcc_invoice_print',
#             'objects': http.request.env['sqcc_invoice_print.sqcc_invoice_print'].search([]),
#         })

#     @http.route('/sqcc_invoice_print/sqcc_invoice_print/objects/<model("sqcc_invoice_print.sqcc_invoice_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sqcc_invoice_print.object', {
#             'object': obj
#         })
