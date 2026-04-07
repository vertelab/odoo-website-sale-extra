{
    'name': 'Website Sale: TIC Age Verification',
    'version': '0.1',
    'summary': 'Makes it easy to verify customer age before finalizing purchase.',
    'category': 'Website',
    'description': """
        Makes it easy to verify customer age before finalizing purchase.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-website/website_sale_tic_age_verification',
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-website',
    'depends': ['base_tic_identity', 'website_sale'],
    'data': [
        'views/website_sale_templates.xml',
    ],
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
