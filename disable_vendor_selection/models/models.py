# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Accountmove(models.Model):
    _inherit = "account.move"

    disable_vendor = fields.Boolean(string='Bill Vendor', help='Read only option for Vendor when the vendor bill created from PO')

    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):
        """
        Override to add Operating Unit from Purchase Order to Invoice.
        """

        purchase_id = self.purchase_id
        if self.purchase_vendor_bill_id.purchase_order_id:
            purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        if purchase_id:
            # Assign OU from PO to Invoice
            self.disable_vendor = True
        return super()._onchange_purchase_auto_complete()


# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"
#
#     def action_view_invoice(self):
#         ks_res = super(PurchaseOrder, self).action_view_invoice()
#         for rec in self:
#             ks_res['disable_vendor'] = True
#         return ks_res