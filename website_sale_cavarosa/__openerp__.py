# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017- Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Website Sale Cavarosa',
    'version': '1.0',
    'category': '',
    'description': """
Special sale configuration for Cavarosa AB
==========================================
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'crm_campaign_supplier',
        'website_crm_campaign',
        'website_product_snippet',
        'website_masonry',
        'cavarosa_delivery',
        'delivery_pickup',
        'website_partner',
        'website_imagemagick',
        'sale_purchase'
    ],
    'data': [
        'views/crm_view.xml',
        'views/res_district_view.xml',
        'views/res_country_view.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        'views/product_template.xml',
        'views/sale_order_line_data.xml',
        'data/cavarosa_data.xml',
        'views/utm_campaign_view.xml',
        # 'data/ir_cron.xml',
    ],
    'qweb': ['static/src/xml/snippets.xml'],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
