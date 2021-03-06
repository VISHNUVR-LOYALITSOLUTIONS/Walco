# -*- coding: utf-8 -*-
{
    'name': "purchase_order_print",

    'summary': """
       PO Print""",

    'description': """
        PO Print
    """,

    'author': "Loyal ItSolutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','report_qweb_pdf_watermark'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/lay_out.xml',
        'views/templates.xml',
        'views/views.xml',

        'views/purchase_print.xml',

        'views/views_header.xml',

        'views/purchase_print_header.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
