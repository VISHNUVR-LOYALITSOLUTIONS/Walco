# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceCurrency(http.Controller):
#     @http.route('/invoice_currency/invoice_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_currency/invoice_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_currency.listing', {
#             'root': '/invoice_currency/invoice_currency',
#             'objects': http.request.env['invoice_currency.invoice_currency'].search([]),
#         })

#     @http.route('/invoice_currency/invoice_currency/objects/<model("invoice_currency.invoice_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_currency.object', {
#             'object': obj
#         })
