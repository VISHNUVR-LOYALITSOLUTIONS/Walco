# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Accountmove(models.Model):
    _inherit = 'account.move'

    client_lpo = fields.Char(string="Client LPO")
    signed_delivery = fields.Char(string="Delivery Number")
    our_ref = fields.Char(string="Our Ref")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    client_lpo = fields.Char(string="Client LPO")

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["client_lpo"] = self.client_lpo
        invoice_vals["our_ref"] = self.name
        return invoice_vals






