# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_code = fields.Char(string="Vendor Code")

    @api.onchange('partner_id')
    def _onchange_purchase_partner(self):
        for i in self:
            if i.partner_id:
                i.vendor_code = i.partner_id.ref

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_code = fields.Char(string="Customer Code")

    @api.onchange('partner_id')
    def _onchange_sale_partner(self):
        for i in self:
            if i.partner_id:
                i.customer_code = i.partner_id.ref

class AccountMove(models.Model):
    _inherit = "account.move"

    partner_code = fields.Char(string="Partner Code")

    @api.onchange('partner_id')
    def _onchange_account_partner(self):
        for i in self:
            if i.partner_id:
                i.partner_code = i.partner_id.ref