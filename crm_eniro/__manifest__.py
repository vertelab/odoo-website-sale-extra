# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
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
    'name': 'CRM Eniro',
    'version': '0.2',
    'category': 'other',
    'license': 'AGPL-3',
    'summary': 'Retrieve leads info from Eniro for crm',
    'description': """
This module adds a search form to retrieve
and company information for leads, ring lists, meetings
or partner with a button for each line in search result.


Depends on partner_eniro
""",
    'author': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['crm','partner_eniro'],
    'data': ['crm_eniro_view.xml'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
