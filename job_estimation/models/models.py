# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models



class CrmLead(models.Model):
    _inherit = 'crm.lead'

    estimate_ids = fields.One2many('sale.estimate.job', 'opportunity_id', string='Estimate')


    def action_estimation_new(self):
        # if not self.partner_id:
        #     return self.env.ref("job_estimation.crm_quotation_partner_action").read()[0]
        # else:
        return self.action_new_estimation()

    def action_new_estimation(self):
        action = self.env.ref("job_estimation.sale_action_estimation_new").read()[0]
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
        }
        return action

