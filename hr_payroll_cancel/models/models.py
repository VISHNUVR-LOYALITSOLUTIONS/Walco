# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    refunded_id = fields.Many2one(
        'hr.payslip',
        string='Refunded Payslip',
        readonly=True
    )

    def refund_sheet(self):
        res = super(HrPayslip, self).refund_sheet()
        self.write({'refunded_id': eval(res['domain'])[0][2][0] or False})
        return res

    def action_payslip_cancel(self):
        for payslip in self:
            if payslip.refunded_id and payslip.refunded_id.state != 'cancel':
                raise ValidationError(_("""To cancel the Original Payslip the
                    Refunded Payslip needs to be canceled first!"""))

            # moves = payslip.mapped('move_id')
            # if moves.filtered(lambda x: x.state == 'posted'):
            #     moves.filtered(lambda x: x.state == 'posted').button_cancel()
            #     moves.unlink()
            if payslip.move_id.journal_id.update_posted:
                if payslip.move_id.state=='draft':
                    payslip.move_id.button_cancel()
                    payslip.move_id.unlink()
            else:
                if payslip.move_id.state == 'draft':
                    payslip.move_id.button_cancel()
                    payslip.move_id.unlink()
                elif payslip.move_id.state == 'posted':
                    self.reverse_payslip_posted_entry()
                    payslip.move_id = False
        return self.write({'state': 'cancel'})

    def reverse_payslip_posted_entry(self):
        """This method is designed to be inherited.
            For example, inherit it if you don't want to start the wizard in
            some scenarios"""

        # view = self.env.ref('account.view_account_move_reversal').id
        for payslip in self:
            wiz = self.env['account.move.reversal'].create(
                {'move_id': payslip.move_id.id,
                 'journal_id':payslip.journal_id.id,
                 'date':payslip.date,
                 'refund_method':'cancel'}
            )
            wiz.reverse_moves()

        return
       