# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerCreationRestriction(http.Controller):
#     @http.route('/customer_creation_restriction/customer_creation_restriction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_creation_restriction/customer_creation_restriction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_creation_restriction.listing', {
#             'root': '/customer_creation_restriction/customer_creation_restriction',
#             'objects': http.request.env['customer_creation_restriction.customer_creation_restriction'].search([]),
#         })

#     @http.route('/customer_creation_restriction/customer_creation_restriction/objects/<model("customer_creation_restriction.customer_creation_restriction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_creation_restriction.object', {
#             'object': obj
#         })
