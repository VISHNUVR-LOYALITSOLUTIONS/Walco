# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EstimateJobType(models.Model):
    _inherit = 'estimate.job.type'

    job_type = fields.Selection(
        selection_add=[
            ('consumable','Consumable'),
            ('logistics','Logistics'),
            ('outsourced','Outsourced'),
            ('other', 'Others')
        ],
        string='Type',
        required=True,
    )
