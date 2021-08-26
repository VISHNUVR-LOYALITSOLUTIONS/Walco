# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Rescompany(models.Model):
    _inherit = 'res.company'

    report_file = fields.Many2one('ir.actions.report',string="Report file")



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    due_on_date = fields.Datetime(string="Due On",store=True)
    destination = fields.Char(string="Destination",store=True)





