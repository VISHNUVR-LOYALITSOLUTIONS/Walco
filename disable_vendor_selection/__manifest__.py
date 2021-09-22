# -*- coding: utf-8 -*-
{
    'name': "disable_vendor_selection",

    'summary': """
            Read option for vendor and invoice when the Bill/Invoice Created by PO/SO""",

    'description': """
           Read option for vendor and invoice when the Bill/Invoice Created by PO/SO
        """,

    'author': "Loyal It Solutions PVT LTD",
    'website': "http://www.loalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','account'],

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
