# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class SaleEstimatelineJob(models.Model):
    _inherit = "sale.estimate.line.job"

    job_type = fields.Selection(
        selection_add=[('consumable','Consumable'),
            ('logistics','Logistics'),
            ('outsourced','Outsourced'),
            ('other', 'Others')
                ],
        string="Type",
        required=True,
    )
