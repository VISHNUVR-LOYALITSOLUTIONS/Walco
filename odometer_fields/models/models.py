# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    purpose = fields.Char(string="Purpose")
    killometer_run = fields.Integer(string="Killometer Run")
