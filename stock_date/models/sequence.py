# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import re
from odoo.addons.base.models import ir_sequence


class IrSequence(models.Model):
    _inherit = 'ir.sequence'


    def _new_sequence_next(self, sequence_date=None):
        """ Returns the next number in the preferred sequence in all the ones given in self."""
        if not self.use_date_range:
            return self._next_do()
        # date mode
        dt = sequence_date or self._context.get('ir_sequence_date', fields.Date.today())
        seq_date = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_from', '<=', dt), ('date_to', '>=', dt)], limit=1)
        if not seq_date:
            seq_date = self._create_date_range_seq(dt)
        return seq_date.with_context(ir_sequence_date_range=seq_date.date_from)._new_sequence_next()

    def _new_sequence_next_by_id(self, sequence_date=None):
        """ Draw an interpolated string using the specified sequence."""
        self.check_access_rights('read')
        return self._new_sequence_next(sequence_date=sequence_date)



class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'


    def _new_sequence_next(self):

        if self.sequence_id.implementation == 'standard':
            number_next = ir_sequence._select_nextval(self._cr,
                                                      'ir_sequence_%03d_%03d' % (self.sequence_id.id, self.id))

            new_number= int(number_next[0])
        else:
            number_next = ir_sequence._update_nogap(self, self.sequence_id.number_increment)
            new_number = number_next

        return self.sequence_id.get_next_char(new_number-1, self.prefix, self.suffix)