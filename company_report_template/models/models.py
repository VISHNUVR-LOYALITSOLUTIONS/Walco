# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = "res.company"

    sale_reports = fields.Selection([
            ('walcotech', 'Walcotech'),
            ('texerv', 'TEXERV'),
            ('walco', 'Walco'),
            ('odoo_standard', 'Odoo Standard'),
        ], default='odoo_standard',string='Sale Print')


