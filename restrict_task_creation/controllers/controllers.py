# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictTaskCreation(http.Controller):
#     @http.route('/restrict_task_creation/restrict_task_creation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_task_creation/restrict_task_creation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_task_creation.listing', {
#             'root': '/restrict_task_creation/restrict_task_creation',
#             'objects': http.request.env['restrict_task_creation.restrict_task_creation'].search([]),
#         })

#     @http.route('/restrict_task_creation/restrict_task_creation/objects/<model("restrict_task_creation.restrict_task_creation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_task_creation.object', {
#             'object': obj
#         })
