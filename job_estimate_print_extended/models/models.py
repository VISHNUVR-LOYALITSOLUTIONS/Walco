# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class job_estimate_print_extended(models.Model):
#     _name = 'job_estimate_print_extended.job_estimate_print_extended'
#     _description = 'job_estimate_print_extended.job_estimate_print_extended'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
