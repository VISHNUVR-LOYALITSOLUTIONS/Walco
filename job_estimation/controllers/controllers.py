# -*- coding: utf-8 -*-
# from odoo import http


# class JobEstimation(http.Controller):
#     @http.route('/job_estimation/job_estimation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/job_estimation/job_estimation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('job_estimation.listing', {
#             'root': '/job_estimation/job_estimation',
#             'objects': http.request.env['job_estimation.job_estimation'].search([]),
#         })

#     @http.route('/job_estimation/job_estimation/objects/<model("job_estimation.job_estimation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('job_estimation.object', {
#             'object': obj
#         })
