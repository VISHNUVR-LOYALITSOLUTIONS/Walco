# -*- coding: utf-8 -*-
{
    'name': "hr_payroll_cancel",

    'summary': """
        hr_payroll_cancel""",

    'description': """
        hr_payroll_cancel
    """,

    'author': "Loyal It Solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr_payroll',
        'hr_payroll_account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
