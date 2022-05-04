# -*- coding: utf-8 -*-
from odoo import models, fields, api
DEFAULT_PRIMARY = '#000000'
DEFAULT_SECONDARY = '#000000'

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    company_watermark = fields.Binary(string="Letterhead", related='company_id.company_watermark', readonly=False)
    rpt_primary_color = fields.Char(related='company_id.rpt_primary_color', readonly=False)
    rpt_secondary_color = fields.Char(related='company_id.rpt_secondary_color', readonly=False)
    rpt_custom_colors = fields.Boolean(compute="_compute_rpt_custom_colors", readonly=False)
    rpt_logo_primary_color = fields.Char(compute="_compute_rpt_logo_colors")
    rpt_logo_secondary_color = fields.Char(compute="_compute_rpt_logo_colors")


    def document_layout_save(self):
        res = super(BaseDocumentLayout, self).document_layout_save()
        for wizard in self:
            wizard.company_id.company_watermark
        return res

    @api.depends('logo')
    def _compute_rpt_logo_colors(self):
        for wizard in self:
            if wizard._context.get('bin_size'):
                wizard_for_image = wizard.with_context(bin_size=False)
            else:
                wizard_for_image = wizard
            wizard.rpt_logo_primary_color, wizard.rpt_logo_secondary_color = wizard_for_image._parse_logo_colors()

    @api.depends('rpt_logo_primary_color', 'rpt_logo_secondary_color', 'rpt_primary_color', 'rpt_secondary_color')
    def _compute_rpt_custom_colors(self):
        for wizard in self:
            rpt_logo_primary = wizard.rpt_logo_primary_color or ''
            rpt_logo_secondary = wizard.rpt_logo_secondary_color or ''
            # Force lower case on color to ensure that FF01AA == ff01aa
            wizard.rpt_custom_colors = (
                    wizard.logo and wizard.rpt_primary_color and wizard.rpt_secondary_color
                    and not (
                    wizard.rpt_primary_color.lower() == rpt_logo_primary.lower()
                    and wizard.rpt_secondary_color.lower() == rpt_logo_secondary.lower()
            )
            )

    @api.onchange('rpt_custom_colors')
    def _onchange_rpt_custom_colors(self):
        for wizard in self:
            if wizard.logo and not wizard.rpt_custom_colors:
                wizard.rpt_primary_color = wizard.rpt_logo_primary_color or DEFAULT_PRIMARY
                wizard.rpt_secondary_color = wizard.rpt_logo_secondary_color or DEFAULT_SECONDARY

