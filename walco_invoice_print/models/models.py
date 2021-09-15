# -*- coding: utf-8 -*-

from num2words import num2words
import logging
import base64
import re
from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_po_issue_date = fields.Date(
        'Customer PO Issue Date',
        copy=False,
        default=fields.date.today(),
    )

    delivery_date = fields.Date(
        'Delivery Date',
        copy=False,
        default=fields.date.today(),
    )

    bank_ids = fields.Many2many(
        comodel_name="res.partner.bank", copy=False, string="Bank Details",
    )


    # client_lpo = fields.Char(string="Client LPO")
    # signed_delivery = fields.Char(string="Delivery Number")
    # our_ref = fields.Char(string="Our Ref")

    def english_amt2words(self,amount, currency, change, precision):
        change_amt = (amount - int(amount)) * pow(10, precision)
        words = '{main_amt} {main_word}'.format(
            main_amt=num2words(int(amount)),
            main_word=currency,
        )
        change_amt = int(round(change_amt))
        # words = words.title()
        if change_amt > 0:
            words += ' and {change_amt} {change_word}'.format(
                change_amt=num2words(change_amt),
                change_word=change,
            )
        words=words.title()
        words = words.replace('And', 'and')
        words = words.replace(',', '')
        return words


class MailComposer(models.TransientModel):

    _inherit = 'mail.compose.message'

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        res = super(MailComposer, self).generate_email_for_composer(template_id, res_ids, fields)
        # res[res_ids[0]]['attachments']=False

        if self.env.context.get('active_model') and self.env.context.get('active_id'):
            active_model = self.env[self.env.context['active_model']].browse(self.env.context['active_id'])
            company_id = active_model.company_id if 'company_id' in active_model else False
            if self.env.context['active_model']=='account.move':
                if active_model:
                    for i in active_model:
                        if company_id.account_reports == 'company':
                            pdf = self.env.ref('walco_invoice_print.walco_invoice_print_menu').sudo().render_qweb_pdf([i.id])[0]
                            pdf = base64.b64encode(pdf)
                            attachments = [('%s.pdf' % i.name, pdf)]
                            res[res_ids[0]]['attachments'] = False
                            res[res_ids[0]]['attachments'] = attachments
                        elif company_id.account_reports == 'odoo_standard':
                            pdf = self.env.ref('account.account_invoices').sudo().render_qweb_pdf([i.id])[0]
                            pdf = base64.b64encode(pdf)
                            attachments = [('%s.pdf' % i.name, pdf)]
                            res[res_ids[0]]['attachments'] = False
                            res[res_ids[0]]['attachments'] = attachments

        return res



