# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = "res.company"

    print_header_img = fields.Binary(string="Header")
    print_footer_img = fields.Binary(string="Footer")
    pdf_watermark = fields.Binary('Watermark')


# class IrActionsReport(models.Model):
#     _inherit = 'ir.actions.report'
#
#     company_id = fields.Many2one('res.company', 'Company', required=True,
#                                  default=lambda self: self.env.user.company)


