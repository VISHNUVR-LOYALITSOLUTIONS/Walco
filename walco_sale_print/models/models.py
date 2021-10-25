# -*- coding: utf-8 -*-

from num2words import num2words
import logging
import base64
import re
from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class MailComposer(models.TransientModel):

    _inherit = 'mail.compose.message'

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        res = super(MailComposer, self).generate_email_for_composer(template_id, res_ids, fields)
        # res[res_ids[0]]['attachments']=False

        if self.env.context.get('active_model') and self.env.context.get('active_id'):
            active_model = self.env[self.env.context['active_model']].browse(self.env.context['active_id'])
            company_id = active_model.company_id if 'company_id' in active_model else False
            if self.env.context['active_model']=='sale.order':
                if active_model:
                    for i in active_model:
                        if company_id.sale_print == 'company':
                            pdf = self.env.ref('walco_sale_print.walco_sale_print_menu').sudo().render_qweb_pdf([i.id])[0]
                            pdf = base64.b64encode(pdf)
                            attachments = [('%s.pdf' % i.name, pdf)]
                            res[res_ids[0]]['attachments'] = False
                            res[res_ids[0]]['attachments'] = attachments
                        elif company_id.sale_print == 'odoo_standard':
                            pdf = self.env.ref('sale.action_report_saleorder').sudo().render_qweb_pdf([i.id])[0]
                            pdf = base64.b64encode(pdf)
                            attachments = [('%s.pdf' % i.name, pdf)]
                            res[res_ids[0]]['attachments'] = False
                            res[res_ids[0]]['attachments'] = attachments

        return res



