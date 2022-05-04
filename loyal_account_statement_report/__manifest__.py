# -*- coding: utf-8 -*-
{
    'name': "Loyal Account Statement Report",

    'summary': """
        STATEMENT OF ACCOUNT""",

    'description': """
      STATEMENT OF ACCOUNT
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",
    'category': 'account',
    'version': '13.0.1',
    'depends': ['base','account', 'report_xlsx'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/base_document_layout_view.xml',
        'views/bank.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/account_statement_pdf.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
