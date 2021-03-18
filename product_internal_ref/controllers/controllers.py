# -*- coding: utf-8 -*-
# from odoo import http


# class ProductInternalRef(http.Controller):
#     @http.route('/product_internal_ref/product_internal_ref/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_internal_ref/product_internal_ref/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_internal_ref.listing', {
#             'root': '/product_internal_ref/product_internal_ref',
#             'objects': http.request.env['product_internal_ref.product_internal_ref'].search([]),
#         })

#     @http.route('/product_internal_ref/product_internal_ref/objects/<model("product_internal_ref.product_internal_ref"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_internal_ref.object', {
#             'object': obj
#         })
