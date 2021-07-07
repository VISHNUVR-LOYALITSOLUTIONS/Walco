# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerReference(http.Controller):
#     @http.route('/partner_reference/partner_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_reference/partner_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_reference.listing', {
#             'root': '/partner_reference/partner_reference',
#             'objects': http.request.env['partner_reference.partner_reference'].search([]),
#         })

#     @http.route('/partner_reference/partner_reference/objects/<model("partner_reference.partner_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_reference.object', {
#             'object': obj
#         })
