# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class SaleEstimatelineJob(models.Model):
    _inherit = "sale.estimate.line.job"

    job_type = fields.Selection(
        selection_add=[('outsourced_vehicle','Outsourced Vehicle'),
            ('outsourced_labour','Outsourced Labour'),

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

    product_group = fields.Many2one('product.group', string="Group")
    product_subgroup = fields.Many2one('product.subgroup', string="Sub Group")
    product_category = fields.Many2one('product.category', string="Category")

    @api.onchange('product_id','product_category','product_group','product_subgroup')
    def onchange_product_id_get_domain(self):

        estimate_productid_list = []
        consumable_productid_list = []
        for i in self:
            if i.job_type=='material' or i.job_type=='consumable':
                if i.product_id:
                    i.product_group = i.product_id.product_group.id
                    i.product_subgroup = i.product_id.product_subgroup.id
                    i.product_category = i.product_id.categ_id

                if i.product_category and not i.product_group and not i.product_subgroup:
                    material_id = self.env["product.product"].search(
                        [('categ_id', '=', i.product_category.id),('product_subgroup', '=', False), ('product_group', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                elif i.product_group and not i.product_subgroup and not i.product_category:
                    material_id = self.env["product.product"].search(
                        [('product_group', '=', i.product_group.id),('product_subgroup', '=', False), ('categ_id', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)

                elif i.product_subgroup and not i.product_group and not i.product_category:
                    material_id = self.env["product.product"].search(
                        [('product_subgroup', '=', i.product_subgroup.id),('product_group', '=', False), ('categ_id', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                elif i.product_category and i.product_group and not i.product_subgroup:
                    material_id = self.env["product.product"].search(
                        [('categ_id', '=', i.product_category.id),('product_group', '=', i.product_group.id),('product_subgroup', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                elif i.product_category and i.product_subgroup and not i.product_group:
                    material_id = self.env["product.product"].search(
                        [('categ_id', '=', i.product_category.id),('product_subgroup', '=', i.product_subgroup.id),('product_group', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                elif i.product_group and i.product_subgroup and not i.product_category:
                    material_id = self.env["product.product"].search(
                        [('product_subgroup', '=', i.product_subgroup.id), ('product_group', '=', i.product_group.id),('categ_id', '=', False)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                elif i.product_group and i.product_subgroup and i.product_category:
                    material_id = self.env["product.product"].search(
                        [('categ_id', '=', i.product_category.id),('product_subgroup', '=', i.product_subgroup.id), ('product_group', '=', i.product_group.id)])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                else:
                    material_id = self.env["product.product"].search([])
                    for line_id in material_id:
                        estimate_productid_list.append(line_id.id)
                result = {'domain': {'product_id': [('id', 'in', estimate_productid_list)]}}
                return result
            # if i.job_type=='consumable':
            #     consumable_id = self.env["product.product"].search(
            #         [('categ_id', '=', i.product_category.id)])
            #     for line_id in consumable_id:
            #         consumable_productid_list.append(line_id.id)
            #     result = {'domain': {'product_id': [('id', 'in', consumable_productid_list)]}}
            #     return result
