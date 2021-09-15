# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = "res.company"

    account_reports = fields.Selection([
            ('company', 'Company'),
            ('odoo_standard', 'Odoo Standard'),
        ], default='odoo_standard',string='Account Print')


