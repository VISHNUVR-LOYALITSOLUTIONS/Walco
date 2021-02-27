# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseConfirmationDate(http.Controller):
#     @http.route('/purchase_confirmation_date/purchase_confirmation_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_confirmation_date/purchase_confirmation_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_confirmation_date.listing', {
#             'root': '/purchase_confirmation_date/purchase_confirmation_date',
#             'objects': http.request.env['purchase_confirmation_date.purchase_confirmation_date'].search([]),
#         })

#     @http.route('/purchase_confirmation_date/purchase_confirmation_date/objects/<model("purchase_confirmation_date.purchase_confirmation_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_confirmation_date.object', {
#             'object': obj
#         })
