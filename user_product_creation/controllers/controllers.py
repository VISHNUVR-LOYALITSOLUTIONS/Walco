# -*- coding: utf-8 -*-
# from odoo import http


# class UserProductCreation(http.Controller):
#     @http.route('/user_product_creation/user_product_creation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/user_product_creation/user_product_creation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('user_product_creation.listing', {
#             'root': '/user_product_creation/user_product_creation',
#             'objects': http.request.env['user_product_creation.user_product_creation'].search([]),
#         })

#     @http.route('/user_product_creation/user_product_creation/objects/<model("user_product_creation.user_product_creation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('user_product_creation.object', {
#             'object': obj
#         })
