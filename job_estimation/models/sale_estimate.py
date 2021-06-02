# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

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


    # tag_ids = fields.Many2many('crm.lead.tag', 'sale_order_tag_rel', 'order_id', 'tag_id', string='Tags')
    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.depends(
        'total',
        'labour_total',
        'overhead_total',
        'consumable_total',
        'logistics_total',
        'outsourced_total',
        'others_total'
    )
    def _compute_job_estimate_total(self):
        for rec in self:
            rec.estimate_total = rec.total + rec.labour_total + rec.overhead_total+rec.consumable_total + rec.logistics_total + rec.outsourced_total +rec.others_total
            
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
        


    # @api.multi
    def estimate_confirm(self):
        res = super(SaleEstimateJob, self).estimate_confirm()
        for rec in self:
            # if not rec.estimate_ids:
            # if not rec.other_estimate_line_ids and not rec.outsourced_estimate_line_ids and not rec.logistics_estimate_line_ids and not rec.consumable_estimate_line_ids:
            #     raise UserError(_('Please enter Estimation Lines!'))
            rec.state = 'confirm'
        return res
            
    # @api.multi
    def estimate_approve(self):
        res= super(SaleEstimateJob, self).estimate_approve()
        for rec in self:
            # if not rec.consumable_estimate_line_ids and not rec.logistics_estimate_line_ids and not rec.outsourced_estimate_line_ids and not rec.other_estimate_line_ids:
            #     raise UserError(_('Please enter Estimation Lines!'))
            rec.state = 'approve'
        return res


    # @api.multi
    def _prepare_quotation_line(self,quotation):
        res = super(SaleEstimateJob, self)._prepare_quotation_line(quotation)
        quo_line_obj = self.env['sale.order.line']
        for rec in self:
            for line in rec.consumable_estimate_line_ids:
                vals1 = {
                                'estimate_bool': line.estimation_bool,
                                'product_id':  line.product_id.id,
                                'product_uom_qty': line.product_uom_qty,
                                'product_uom': line.product_uom.id,
                                'price_unit' : line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'name' : line.product_description,
                                'price_total' : self.total,
                                'discount' : line.discount,
                                'order_id':quotation.id,
                                }
                quo_line = quo_line_obj.create(vals1)
            for line in rec.logistics_estimate_line_ids:
                vals1 = {
                                'estimate_bool': line.estimation_bool,
                                'product_id':  line.product_id.id,
                                'product_uom_qty': line.product_uom_qty,
                                # 'product_uom': line.product_uom.id,
                                'product_uom': line.product_id.uom_id.id,
                                'price_unit' : line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'name' : line.product_description,
                                'price_total' : self.total,
                                'discount' : line.discount,
                                'order_id':quotation.id,
                                }
                quo_line = quo_line_obj.create(vals1)
                
            for line in rec.outsourced_estimate_line_ids:
                vals1 = {
                                'estimate_bool': line.estimation_bool,
                                'product_id':  line.product_id.id,
                                'product_uom_qty': line.product_uom_qty,
                                'product_uom': line.product_uom.id,
                                'price_unit' : line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'name' : line.product_description,
                                'price_total' : self.total,
                                'discount' : line.discount,
                                'order_id':quotation.id,
                                }
                quo_line = quo_line_obj.create(vals1)

            for line in rec.other_estimate_line_ids:
                vals1 = {
                                'estimate_bool': line.estimation_bool,
                                'product_id':  line.product_id.id,
                                'product_uom_qty': line.product_uom_qty,
                                'product_uom': line.product_uom.id,
                                'price_unit' : line.price_unit,
                                'price_subtotal': line.price_subtotal,
                                'name' : line.product_description,
                                'price_total' : self.total,
                                'discount' : line.discount,
                                'order_id':quotation.id,
                                }
                quo_line = quo_line_obj.create(vals1)
        return res
        

            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
