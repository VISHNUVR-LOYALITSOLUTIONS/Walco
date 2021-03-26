# -*- coding: utf-8 -*-
{
    'name': "Purchase Order Approval",

    'summary': """
        Purchase Order Approval
            1.Operation manager approval
            2.Director approval
            3.Purchase director approval
            4. Finance manager approval
        """,

    'description': """
        Purchase Order Approval
            1.Operation manager approval
            2.Director approval
            3.Purchase director approval
            4. Finance manager approval
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/approval_security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
