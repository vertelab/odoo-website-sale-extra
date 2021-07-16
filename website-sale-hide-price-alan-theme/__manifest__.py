# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<http://vertel.se>).
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
    'name': 'website-sale-hide_price_alan_theme',
    'version': '12.0.1.0',
    # ~ 'license': 'AGPL-3',
    'author': ' Vertel AB',
    'website': 'http://vertel.se',
    'category': 'website',
    'description': """ 
    This module makes sure that the price is invisible on the sale page if the user is logged out and if the website uses the alan theme.
    """,
    'depends': ['website_hide_price_public_user','alan_customize'],
    'data': ['views/website_template_alan_theme.xml',
    ],
    'installable': 'True',
    'application': 'False',
    'auto_install': 'True',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
