# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = "res.company"

    sale_print = fields.Selection([
            ('company', 'Company'),
            ('odoo_standard', 'Odoo Standard'),
        ], default='odoo_standard',string='Sale Order Print')


