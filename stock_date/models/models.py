# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import re


class Picking(models.Model):
    _inherit = "stock.picking"

    stock_force_date = fields.Datetime(string='Date')

    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        for i in self:
            if i.scheduled_date:
                i.stock_force_date = i.scheduled_date

    @api.model
    def create(self, vals):
        res = super(Picking, self).create(vals)
        defaults = self.default_get(['name', 'picking_type_id'])
        picking_type = self.env['stock.picking.type'].browse(
            vals.get('picking_type_id', defaults.get('picking_type_id')))
        seq_date = None
        current_date = fields.Date.today()
        if vals['stock_force_date']:
            current_date = fields.Datetime.to_datetime(vals['stock_force_date']).date()
        if 'stock_force_date' in vals and fields.Date.today() != current_date:
            seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['stock_force_date']))

            res.update({'name':picking_type.sequence_id._new_sequence_next_by_id(
                sequence_date=seq_date
            )})
        # vals['name'] =

        return res




class SaleOrder(models.Model):
    _inherit = "sale.order"

    stock_date = fields.Datetime(string='Date')

    @api.onchange('stock_date','date_order')
    def _onchange_stock_date(self):
        for i in self:
            # if i.stock_date:
            i.stock_date = i.date_order

    def action_confirm(self):


        for order in self:
            order.write({
                'stock_date': order.date_order,

            })
            order.picking_ids.write({

                'scheduled_date': order.stock_date,
                'stock_force_date': order.stock_date,
                # 'stock_force_date': order.date_order,

                                     })

        return super(SaleOrder, self).action_confirm()

    def _action_confirm(self):
        """ On SO confirmation, some lines should generate a task or a project. """
        result = super(SaleOrder, self)._action_confirm()
        for order in self:

            order.picking_ids.write({

                'scheduled_date': order.stock_date,
                'stock_force_date': order.stock_date,
                # 'stock_force_date': order.date_order,

            })
        return result

class confirmationState(models.TransientModel):
    _inherit = 'confirmation.date'

    def confirm(self):
        for order in self:
            order.sale_id.picking_ids.write({
                                    'scheduled_date': order.confirmation_date,
                                    'stock_force_date': order.confirmation_date

                                     })
        return super(confirmationState, self).confirm()


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res.update({
            'scheduled_date':self.date_order,
            'stock_force_date':self.date_order
        })
        return res

    # def _create_stock_moves(self, picking):
    #     res = super(PurchaseOrder, self)._create_stock_moves()
    #     # for purchase in res:
    #     for picking in self.picking_ids:
    #         picking.update({
    #                 'scheduled_date': self.date_order,
    #                 'stock_force_date': self.date_order
    #             })
    #     return res


    def _create_picking(self):
        res = super(PurchaseOrder, self)._create_picking()
        for i in self.picking_ids:
            i.write({
                'scheduled_date': self.date_order,
                'stock_force_date': self.date_order
            })

        return res

# class StockRuleInherit(models.Model):
#     _inherit = 'stock.rule'
#
#     def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
#         res = super(StockRuleInherit, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
#                                                            name, origin, values, group_id)
#         res['stock_force_date'] = group_id['group_id'].sale_id.stock_date
#         res['scheduled_date'] = group_id['group_id'].sale_id.stock_date
#         return res

class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals['stock_force_date'] = self.mapped('sale_line_id.order_id.stock_date')[0]
        vals['scheduled_date'] = self.mapped('sale_line_id.order_id.stock_date')[0]
        return vals