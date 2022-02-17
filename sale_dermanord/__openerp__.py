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
    'name': 'Sale Dermanord',
    'version': '1.0',
    'category': '',
    'description': """
Special order imports for Dermanord AB
======================================
* Fina mig i Hedemora AB (pdf)
* Lyko Online AB (Excel)
* SKINCITY SWEDEN AB (pdf)
* Isaksen & CO AS (Excel)
* Nordic Web Trading AB (Excel)
* Eckerö Group - Rederiaktiebolaget Eckerö (Birka) (Text)
* Tailwide AB (Narutligt snygg) (Url)
* Åhlens AB (Url)
* Kicks (Url)

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['sale',],
    'external_dependencies': {
        'python': ['xlrd','pdfminer','unicodecsv'],
    },
    'data': [
        'order_import_view.xml',
        ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
