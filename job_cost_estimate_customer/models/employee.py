# -*- coding: utf-8 -*-

from odoo import api,models, fields

class SaleOrder(models.Model):

    _inherit = "sale.order"

    markup = fields.Float(string='Markup', store=True)
    overhead_amount = fields.Float(string='Overhead Amount', store=True)

    @api.depends('order_line.price_total', 'markup', 'overhead_amount')
    def _amount_all(self):
        res = super(SaleOrder, self)._amount_all()
        for rec in self:
            if rec.markup !=0 :
                rec.amount_total = ((rec.amount_untaxed + rec.amount_tax)* (rec.markup/100))
            rec.amount_total = rec.amount_total + rec.overhead_amount
        return res


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    estimate_bool = fields.Boolean(default=False)

class HrEmployeePrivate(models.Model):

    _inherit = "hr.employee"

    hourly_cost = fields.Float(string="Hourly Cost")
    product_id = fields.Many2one('product.product',string='Related Product',)

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    price_per_kilometer = fields.Float(string="Price/Km")
    product_id = fields.Many2one('product.product',string='Related Product',)