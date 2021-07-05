# -*- coding: utf-8 -*-
{
    'name': "payslip_expense_reference",

    'summary': """
        Expense Reference in payslip,
        cancel the readonly field from leave """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Loyal It Solutions PVt LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_holidays','hr_payroll_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
