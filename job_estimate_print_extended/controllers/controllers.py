# -*- coding: utf-8 -*-
# from odoo import http


# class JobEstimatePrintExtended(http.Controller):
#     @http.route('/job_estimate_print_extended/job_estimate_print_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/job_estimate_print_extended/job_estimate_print_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('job_estimate_print_extended.listing', {
#             'root': '/job_estimate_print_extended/job_estimate_print_extended',
#             'objects': http.request.env['job_estimate_print_extended.job_estimate_print_extended'].search([]),
#         })

#     @http.route('/job_estimate_print_extended/job_estimate_print_extended/objects/<model("job_estimate_print_extended.job_estimate_print_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('job_estimate_print_extended.object', {
#             'object': obj
#         })
