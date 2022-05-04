# -*- coding: utf-8 -*-

from odoo import models, fields, api
class ResBank(models.Model):
    _inherit = 'res.bank'

    name_arabic = fields.Char('Name In Arabic')
