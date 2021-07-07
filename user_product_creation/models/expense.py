# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import Warning, RedirectWarning



class ProductProduct(models.Model):
    _inherit = 'hr.expense'

    sub_product_id = fields.Many2one('product.product',string="Sub Product")


    @api.onchange('product_id' ,'sub_product_id')
    def onchange_product_id_get_domain(self):
        for i in self:
            subproduct_list = []
            mainproduct_list = []
            subproduct_id = self.env["product.product"].search([('sub_product', '=', True)])
            mainproduct_id = self.env["product.product"].search([('sub_product', '=', False),('can_be_expensed', '=', True),])
            for main_line_id in mainproduct_id:
                mainproduct_list.append(main_line_id.id)
            for line_id in subproduct_id:
                subproduct_list.append(line_id.id)
            result = \
                {'domain': {'product_id': [('id', 'in', mainproduct_list),], 'sub_product_id': [('id', 'in', subproduct_list)]}}
            return result
