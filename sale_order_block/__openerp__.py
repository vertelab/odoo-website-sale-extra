# -*- coding: utf-8 -*-
{
    'name': "sale_order_block",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Vertel AB",
    'website': "http://www.vertel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website', 'sale','crm','website_hr_cv','website_crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'sale_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['sale_demo.xml',
    ],
}
