# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Pdf watermark",
    "version": "13.0.1.0.1",
    "author": "Therp BV, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "summary": "Add watermarks to your QWEB PDF reports",
    "website": "https://github.com/oca/reporting-engine",
    "depends": [
        'web', 'header_footer_company'
    ],
    "data": [
        "demo/report.xml",
        "views/ir_actions_report_xml.xml",
        "views/layout_templates.xml",
    ],
    "demo": [
        "demo/report.xml"
    ],
    "installable": True,
    'external_dependencies': {
        'python': [
            'PyPDF2',
        ],
    },
}
