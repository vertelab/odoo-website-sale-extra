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
    'website': 'http://www.vertel.se',
    'depends': ['crm_campaign_supplier', 'website_crm_campaign', 'website_product_snippet', 'website_masonry', 'cavarosa_delivery', 'delivery_pickup', 'sale_order_line_view'],
    'data': [
        'crm_view.xml',
        'res_district_view.xml',
        'res_country_view.xml',
        'res_partner_view.xml',
        'product_view.xml',
        'product_template.xml',
        'report_sale_order_line.xml',
        'sale_order_line_data.xml',
        'security/ir.model.access.csv',
        ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
