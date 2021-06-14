# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GroupProduct(models.Model):
    _name = 'product.group'

    name= fields.Char(String="Name")

class SubGroupProduct(models.Model):
    _name = 'product.subgroup'

    name= fields.Char(String="Name")



