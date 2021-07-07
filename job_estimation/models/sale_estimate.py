# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_group = fields.Many2one('product.group',string="Group")
    product_subgroup = fields.Many2one('product.subgroup', string="Sub Group")

    job_type = fields.Selection(
        selection=[('material', 'Material'),
                   ('consumable', 'Consumable'),
                   ],
        string="Type",

    )


class SaleEstimateJob(models.Model):
    _inherit = "sale.estimate.job"



    consumable_estimate_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type','=','consumable')],
    )

    logistics_estimate_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'logistics')],
    )

    outsourced_estimate_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'outsourced')],
    )
    other_estimate_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'other')],
    )

    post_estimate_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'estimation')],
    )

    outsourced_labour_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'outsourced_labour')],
    )

    outsourced_vehicle_line_ids = fields.One2many(
        'sale.estimate.line.job',
        'estimate_id',
        'Estimate Lines',
        copy=True,
        domain=[('job_type', '=', 'outsourced_vehicle')],
    )

    consumable_total = fields.Float(
        compute='_compute_consumable_total',
        string='Total Consumable Estimate',
        store=True
    )
    logistics_total = fields.Float(
        compute='_compute_logistics_total',
        string='Total Logistics Estimate',
        store=True
    )

    outsourced_total = fields.Float(
        compute='_compute_outsourced_total',
        string='Total Outsourced Estimate',
        store=True
    )

    others_total = fields.Float(
        compute='_compute_others_total',
        string='Total Others Estimate',
        store=True
    )

    outsourced_labour_total = fields.Float(
        compute='_compute_outsourced_labour',
        string='Total Outsourced Labour',
        store=True
    )

    outsourced_vehicle_total = fields.Float(
        compute='_compute_outsourced_vehicle',
        string='Total Outsourced vehicle',
        store=True
    )


    # tag_ids = fields.Many2many('crm.lead.tag', 'sale_order_tag_rel', 'order_id', 'tag_id', string='Tags')
    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    markup = fields.Float(string='Total Markup', compute='_compute_total_markup',
                          store=True, )

    @api.depends('post_estimate_line_ids.markup_value')
    def _compute_total_markup(self):
        for rec in self:
            rec.markup = 0.0
            for line in rec.post_estimate_line_ids:
                rec.markup += line.markup_value

    @api.depends(
        'total',
        'labour_total',
        'overhead_total',
        'consumable_total',
        'logistics_total',
        'outsourced_total',
        'others_total',
        'outsourced_labour_total',
        'outsourced_vehicle_total',
    )
    def _compute_job_estimate_total(self):
        for rec in self:
            rec.estimate_total = rec.total + rec.labour_total + rec.overhead_total+rec.consumable_total + rec.logistics_total + rec.outsourced_total + rec.outsourced_labour_total + rec.outsourced_vehicle_total
                                 # +rec.others_total
            
    @api.depends('consumable_estimate_line_ids.price_subtotal')
    def _compute_consumable_total(self):
        for rec in self:
            rec.consumable_total = 0.0
            for line in rec.consumable_estimate_line_ids:
                rec.consumable_total += line.price_subtotal
                
    @api.depends('logistics_estimate_line_ids.price_subtotal')
    def _compute_logistics_total(self):
        for rec in self:
            rec.logistics_total = 0.0
            for line in rec.logistics_estimate_line_ids:
                rec.logistics_total += line.price_subtotal

    @api.depends('outsourced_estimate_line_ids.price_subtotal')
    def _compute_outsourced_total(self):
        for rec in self:
            rec.outsourced_total = 0.0
            for line in rec.outsourced_estimate_line_ids:
                rec.outsourced_total += line.price_subtotal

    @api.depends('other_estimate_line_ids.price_subtotal')
    def _compute_others_total(self):
        for rec in self:
            rec.others_total = 0.0
            for line in rec.other_estimate_line_ids:
                rec.others_total += line.price_subtotal

    @api.depends('outsourced_vehicle_line_ids.price_subtotal')
    def _compute_outsourced_vehicle(self):
        for rec in self:
            rec.outsourced_vehicle_total = 0.0
            for line in rec.outsourced_vehicle_line_ids:
                rec.outsourced_vehicle_total += line.price_subtotal

    @api.depends('outsourced_labour_line_ids.price_subtotal')
    def _compute_outsourced_labour(self):
        for rec in self:
            rec.outsourced_labour_total = 0.0
            for line in rec.outsourced_labour_line_ids:
                rec.outsourced_labour_total += line.price_subtotal
        


    # @api.multi
    def estimate_confirm(self):
        post_list = []
        for rec in self:

            for line in rec.estimate_ids:
                vals1 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon1 = (0, 0, vals1)
                post_list.append(mon1)
                # post_list.append([0, 0, vals1])
            for line in rec.labour_estimate_line_ids:
                vals2 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon2 = (0, 0, vals2)
                post_list.append(mon2)
                # post_list.append([0, 0, vals2])
            for line in rec.overhead_estimate_line_ids:
                vals3 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon3 = (0, 0, vals3)
                post_list.append(mon3)
                # post_list.append([0, 0, vals3])
            for line in rec.consumable_estimate_line_ids:
                vals4 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon4 = (0, 0, vals4)
                post_list.append(mon4)
                # post_list.append([0, 0, vals4])
            for line in rec.logistics_estimate_line_ids:
                vals5 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon5 = (0, 0, vals5)
                post_list.append(mon5)
                # post_list.append([0, 0, vals5])

            for line in rec.outsourced_estimate_line_ids:
                vals6 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon6 = (0, 0, vals6)
                post_list.append(mon6)
                # post_list.append([0, 0, vals6])
            for line in rec.outsourced_labour_line_ids:
                vals7 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon7 = (0, 0, vals7)
                post_list.append(mon7)
            for line in rec.outsourced_vehicle_line_ids:
                vals8 = {
                    'job_type': 'estimation',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'product_description': line.product_description,
                    # 'total': self.total,
                    'discount': line.discount,
                }
                mon8 = (0, 0, vals8)
                post_list.append(mon8)

            # post_list.append([0, 0, val])
            self.post_estimate_line_ids = [(6, 0, [])]
            self.write({'post_estimate_line_ids': post_list})

        return super(SaleEstimateJob, self).estimate_confirm()
            
    # @api.multi
    # def estimate_approve(self):
    #     res= super(SaleEstimateJob, self).estimate_approve()
    #     for rec in self:
    #         # if not rec.consumable_estimate_line_ids and not rec.logistics_estimate_line_ids and not rec.outsourced_estimate_line_ids and not rec.other_estimate_line_ids:
    #         #     raise UserError(_('Please enter Estimation Lines!'))
    #         rec.state = 'approve'
    #     return res


    # @api.multi
    def _prepare_quotation_line(self,quotation):
        res = super(SaleEstimateJob, self)._prepare_quotation_line(quotation)
        quo_line_obj = self.env['sale.order.line']
        for rec in self:

            for line in rec.other_estimate_line_ids:
                no_lines = len(rec.other_estimate_line_ids)
                estimate_total = ((line.price_unit/rec.estimate_total)*rec.markup + line.price_unit) if rec.total!=0 else 0


                vals1 = {
                                'estimate_bool': line.estimation_bool,
                                'product_id':  line.product_id.id,
                                'product_uom_qty': line.product_uom_qty,
                                'product_uom': line.product_uom.id,
                                'price_unit' : estimate_total,
                                # 'price_subtotal': estimate_total,
                                'name' : line.product_description,
                                'price_total' : self.total,
                                'discount' : line.discount,
                                'order_id':quotation.id,
                                'job_type': 'estimation',
                                # 'markup': rec.markup/no_lines if no_lines!=0 else 0,
                                }
                quo_line = quo_line_obj.create(vals1)
        return res
        

            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
