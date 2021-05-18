# -*- coding: utf-8 -*-

from odoo import api,models, fields

class UpdateEstimation(models.TransientModel):
    _name = 'estimation.approval'

    markup = fields.Float(string='Markup', store=True)
    overhead_amount = fields.Float(string='Overhead Amount', store=True)
    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        oldname='payment_term'
    )
    estimate_id = fields.Many2one(
        'sale.estimate.job',
        string='Sale Estimate',readonly=True
    )

    @api.model
    def _prepare_default_get(self, estimation):
        default = {
            'estimate_id': estimation.id,
            'markup': estimation.markup,
            'overhead_amount': estimation.overhead_amount,
            'payment_term_id':estimation.payment_term_id.id

        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(UpdateEstimation, self).default_get(fields)
        assert self._context.get('active_model') == 'sale.estimate.job', \
            'active_model should be sale.estimate.job'
        estimation = self.env['sale.estimate.job'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(estimation)
        res.update(default)
        return res

    def _prepare_update_so(self):
        self.ensure_one()
        return {
            'payment_term_id': self.payment_term_id.id,
            'markup':  self.markup,
            'overhead_amount': self.overhead_amount,
            'state' :'approve'

        }

    def confirm(self):
        self.ensure_one()

        vals = self._prepare_update_so()
        self.estimate_id.write(vals)
        return True