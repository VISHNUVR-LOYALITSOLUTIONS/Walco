# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

# if worked_days.OTH.number_of_hours and contract.wage:
#     result=(((contract.wage/31) / 8) * ( worked_days.OTH.number_of_hours)) * 1.50


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    expense_reference = fields.Char(string="Reference")


#
class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    expense_reference = fields.Char(string="Reference")

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    @api.onchange('expense_sheet_ids')
    def _onchange_expense_sheet_ids(self):

        res = super(HrPayslip, self)._onchange_expense_sheet_ids()
        expense_type = self.env.ref('hr_payroll_expense.expense_other_input', raise_if_not_found=False)

        if self.expense_sheet_ids:
            reference = ', '.join(
                picking.expense_reference for picking in self.expense_sheet_ids if picking.expense_reference != False)
            lines_to_keep = self.input_line_ids.filtered(lambda x: x.input_type_id == expense_type)
            # input_lines_vals = [(5, 0, 0)] + [(4, line.id, False) for line in lines_to_keep]
            lines_to_keep.write({
                'expense_reference': reference,
            })


        return res