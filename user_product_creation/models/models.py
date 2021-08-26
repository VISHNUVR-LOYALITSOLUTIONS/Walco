# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import Warning, RedirectWarning



class ProductProduct(models.Model):
    _inherit = 'product.product'


    @api.model
    def create(self, vals):
        if self.env.user.has_group('user_product_creation.user_restrict_product_creation'):
            raise Warning(
                _('Sorry, you are not allowed to create new products.'),
            )
        else:
            return super(ProductProduct, self).create(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sub_product = fields.Boolean(string="Sub Product")


    @api.model
    def create(self, vals):
        if self.env.user.has_group('user_product_creation.user_restrict_product_creation'):
            raise Warning(
                _('Sorry, you are not allowed to create new products.'),
            )
        else:
            return super(ProductTemplate, self).create(vals)
