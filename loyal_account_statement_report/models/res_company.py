# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Company(models.Model):
    _inherit = "res.company"

    company_watermark = fields.Binary(string="Letter Head")
    rpt_primary_color = fields.Char(readonly=False)
    rpt_secondary_color = fields.Char(readonly=False)
    # company_watermark_expression = fields.Char(
    #     'Watermark expression', help='An expression yielding the base64 '
    #                                  'encoded data to be used as watermark. \n'
    #                                  'You have access to variables `env` and `docs`')
    #
