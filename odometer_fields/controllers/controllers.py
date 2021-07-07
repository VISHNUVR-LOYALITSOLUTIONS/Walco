# -*- coding: utf-8 -*-
# from odoo import http


# class OdometerFields(http.Controller):
#     @http.route('/odometer_fields/odometer_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odometer_fields/odometer_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odometer_fields.listing', {
#             'root': '/odometer_fields/odometer_fields',
#             'objects': http.request.env['odometer_fields.odometer_fields'].search([]),
#         })

#     @http.route('/odometer_fields/odometer_fields/objects/<model("odometer_fields.odometer_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odometer_fields.object', {
#             'object': obj
#         })
