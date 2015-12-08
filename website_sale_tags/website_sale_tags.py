# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
from openerp.addons.website_sale.controllers.main import website_sale
import werkzeug
import pytz
import re


import logging
_logger = logging.getLogger(__name__)

class product_tags(http.Controller):
    _inherit = "website_product_tags.product_template"

    @http.route(['/shop/<model("img.tag"):tags>'], type='http', auth='public', website='True')
    def tagged_products(self, **post):
        return request.render('website_sale.product', {'product': request.env['product.template'].sudo().search([('image_tags', '=', tags)], order='website_sequence')})


class website_sale(website_sale):
    
    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|','|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                    ('image_tags', 'ilike', srch)]
        
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]
        
        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        #~ _logger.warning('<<<<<<<<<<<<<< DOMAIN: %s' %domain)

        return domain
