# -*- coding: utf-8 -*-
{
    'name': 'XKL Sale Quote PDF Report',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Generates a professional XKL-branded proposal PDF from the Sale Order form',
    'description': """
XKL Sale Quote PDF Report
==========================
Adds a "Print XKL Proposal" button to the Sale Order form.
Generates a multi-page branded PDF proposal including:

- Page 1  : Cover page
- Page 2  : Introduction, Strategic Objectives, Conclusion
- Page 3  : XKL History & Innovation
- Page 4  : Customer Requirements
- Page 5  : Customized Solution
- Page 6  : Future Upgrades
- Page 7  : Sales Order Form (line items, pricing, totals)

All content is driven by fields configured directly on the Sale Order
and its order lines — no external data needed.
    """,
    'author': 'XKL LLC',
    'website': 'https://www.xkl.com',
    'license': 'LGPL-3',
    'depends': ['sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'report/sale_quote_report.xml',
        'report/sale_quote_template.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
