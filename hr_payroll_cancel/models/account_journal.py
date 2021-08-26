# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval

class AccountJournal(models.Model):
    _inherit = "account.journal"

    update_posted = fields.Boolean(string='Allow Cancelling Entries',
        help="Check this box if you want to allow the cancellation the entries related to this journal or of the invoice related to this journal")