# -*- coding: utf-8 -*-
# from odoo import http


# class DisableVendorSelection(http.Controller):
#     @http.route('/disable_vendor_selection/disable_vendor_selection/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/disable_vendor_selection/disable_vendor_selection/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('disable_vendor_selection.listing', {
#             'root': '/disable_vendor_selection/disable_vendor_selection',
#             'objects': http.request.env['disable_vendor_selection.disable_vendor_selection'].search([]),
#         })

#     @http.route('/disable_vendor_selection/disable_vendor_selection/objects/<model("disable_vendor_selection.disable_vendor_selection"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('disable_vendor_selection.object', {
#             'object': obj
#         })
