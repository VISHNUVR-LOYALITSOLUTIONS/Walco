# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    internal_ref = fields.Char(string="Internal Reference")


    def _prepare_account_move_line(self, move):
        res =super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res['internal_ref'] = self.product_id.default_code
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLine, self).onchange_product_id()
        self.internal_ref = self.product_id.default_code
        return res
