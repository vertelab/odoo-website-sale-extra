# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
import odoo
import werkzeug
import logging
_logger = logging.getLogger(__name__)


class product_snippet(http.Controller):

    @http.route(['/product_snippet/product_change'], type='json', auth="user", website=True)
    def product_change(self, product=None, **kw):
        product = request.env['product.template'].browse(int(product))
        return {'id': product.id, 'name': product.name, 'image': product.image_medium, 'description': product.description_sale}

    @http.route(['/product_snippet/get_products'], type='json', auth="user", website=True)
    def get_products(self, **kw):
        products = request.env['product.template'].search([('website_published', '=', True)])
        products_list = {}
        for p in products:
            products_list[p.id] = p.name
        return products_list

    @http.route(['/product_snippet/get_products_by_category'], type='json', auth="user", website=True)
    def get_products_by_category(self, categ_id=None, **kw):
        category = request.env['product.category'].browse(int(categ_id))
        products = request.env['product.template'].search([('categ_id', '=', int(categ_id)), ('website_published', '=', True)])
        products_list = {'category': category.name, 'products': {}}
        for p in products:
            products_list['products'][p.id] = {'name': p.name, 'image': p.image_medium, 'description': p.description_sale if p.description_sale else ''}
            _logger.warning('sandra %s' % product_list)
        return products_list

    @http.route(['/product_snippet/get_products_by_partner'], type='json', auth="user", website=True)
    def get_products_by_partner(self, partner_id=None, **kw):
        partner = request.env['res.partner'].browse(int(partner_id))
        products = request.env['res.partner'].search([('id', '=', int(partner_id))]).product_ids.filtered(lambda p: p.website_published == True)
        products_list = {'partner': partner.name, 'products': {}}
        for p in products:
            products_list['products'][p.id] = {'name': p.name, 'image': p.image_medium, 'description': p.description_sale if p.description_sale else ''}
        return products_list
