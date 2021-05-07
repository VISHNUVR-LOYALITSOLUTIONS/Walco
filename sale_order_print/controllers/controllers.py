# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderPrint(http.Controller):
#     @http.route('/purchase_order_print/purchase_order_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_print/purchase_order_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_print.listing', {
#             'root': '/purchase_order_print/purchase_order_print',
#             'objects': http.request.env['purchase_order_print.purchase_order_print'].search([]),
#         })

#     @http.route('/purchase_order_print/purchase_order_print/objects/<model("purchase_order_print.purchase_order_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_print.object', {
#             'object': obj
#         })
