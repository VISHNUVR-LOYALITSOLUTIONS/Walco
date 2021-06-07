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
            ('estimation','Estimation'),
            ('other', 'Others')
                ],
        string="Type",
        required=True,
    )

    markup = fields.Float(string='Markup', store=True)

    @api.depends('price_unit', 'product_uom_qty', 'discount','markup_value','markup')
    def _compute_amount(self):
        res = super(SaleEstimatelineJob, self)._compute_amount()
        for rec in self:

            if rec.job_type=='estimation':
                if rec.markup:
                    rec.markup_value = (rec.price_unit * rec.product_uom_qty) * rec.markup / 100
                    rec.price_subtotal = rec.price_unit * rec.product_uom_qty + rec.markup_value

                else:
                    rec.price_subtotal = rec.price_unit * rec.product_uom_qty +rec.markup_value
        return res

    markup_value = fields.Float(
        compute='_compute_amount',
        string='Markup Value',
        store=True
    )
