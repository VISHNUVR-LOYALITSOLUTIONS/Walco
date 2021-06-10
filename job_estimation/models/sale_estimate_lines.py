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

    @api.onchange('product_id')
    def onchange_product_id_get_domain(self):

        estimate_productid_list = []
        consumable_productid_list = []
        if self.job_type=='material':
            material_id = self.env["product.product"].search(
                [('job_type', '=', 'material')])
            for line_id in material_id:
                estimate_productid_list.append(line_id.id)
            result = {'domain': {'product_id': [('id', 'in', estimate_productid_list)]}}
            return result
        if self.job_type=='consumable':
            consumable_id = self.env["product.product"].search(
                [('job_type', '=', 'consumable')])
            for line_id in consumable_id:
                consumable_productid_list.append(line_id.id)
            result = {'domain': {'product_id': [('id', 'in', consumable_productid_list)]}}
            return result
