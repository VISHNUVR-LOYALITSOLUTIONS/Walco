# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # confirmation_date = fields.Datetime(string="Confirmation Date",store=True)

    def purchase_confirm_wizard_button(self):
        """This method is designed to be inherited.
        For example, inherit it if you don't want to start the wizard in
        some scenarios"""
        action = self.env.ref(
            'purchase_confirmation_date.purchase_update_confirmation_date_action').read()[0]
        return action


class PurchaseconfirmationState(models.TransientModel):
    _name = 'purchase.confirmation.date'

    confirmation_date = fields.Datetime(string="Confirmation Date",store=True)

    purchase_id = fields.Many2one(
        'purchase.order', string='Purchase Order', readonly=True)


    @api.model
    def _prepare_default_get(self, order):
        default = {
            'purchase_id': order.id,
            'confirmation_date': order.date_order,

        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(PurchaseconfirmationState, self).default_get(fields)
        assert self._context.get('active_model') == 'purchase.order', \
            'active_model should be purchase.order'
        order = self.env['purchase.order'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        res.update(default)
        return res

    def _prepare_update_so(self):
        self.ensure_one()
        return {
            'date_order': self.confirmation_date,
            'date_approve':self.confirmation_date,
        }

    def confirm(self):
        self.ensure_one()
        # confirm sale order
        self.purchase_id.button_confirm()
        vals = self._prepare_update_so()
        self.purchase_id.write(vals)
        return True