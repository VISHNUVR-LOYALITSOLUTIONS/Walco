# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_approval = fields.Boolean(default=False, string='PO Approval')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('waiting_for_manager_approval', 'Manager Approval'),
                                            ('waiting_for_director_approval', 'Director Approval'),
                                            ('waiting_for_purchase_director_approval', 'Purchase Director Approval'),
                                            ('waiting_for_financial_approval', 'Financial Approval'),
                                            ('refused', 'Refused')])

    def button_confirm(self):
        for order in self:
            if not order.company_id.po_approval:
                res = super(PurchaseOrder, self).button_confirm()
            else:
                if order.state in ['waiting_for_financial_approval']:
                    if order.env.user.user_has_groups('purchase_order_approval.group_finance_manager'):
                        order._add_supplier_to_product()
                        # Deal with double validation process
                        if order.company_id.po_double_validation == 'one_step' \
                            or (order.company_id.po_double_validation == 'two_step' \
                                and order.amount_total < self.env.company.currency_id._convert(
                                order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                                order.date_order or fields.Date.today())) \
                                or order.user_has_groups('purchase.group_purchase_manager'):
                            order.button_approve()
                        else:
                            order.write({'state': 'to approve'})
                        res = True
                    else:
                        raise UserError(_(
                            "Your are not allowed to confirm the purchase order."))
                else:
                    res = True
                    if order.env.user.user_has_groups('purchase_order_approval.group_operation_manager'):
                        order.write({'state': 'waiting_for_director_approval'})
                        continue
                    else:
                        order.write({'state': 'waiting_for_manager_approval'})
                        continue
            return res

    def button_manager_approval(self):
        for order in self:
            order.write({'state': 'waiting_for_director_approval'})

    def button_director_approval(self):
        for order in self:
            order.write({'state': 'waiting_for_purchase_director_approval'})

    def button_purchase_director_approval(self):
        for order in self:
            order.write({'state': 'waiting_for_financial_approval'})

    def button_refuse(self):
        for order in self:
            order.write({'state': 'refused'})



