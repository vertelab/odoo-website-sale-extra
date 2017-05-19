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
from openerp import models, fields, api, _
from openerp import http
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = 'res.partner'

    district_id = fields.Many2one(comodel_name='res.district', string='District')
    campaign_ids = fields.Many2many(string='Campaigns', comodel_name='crm.tracking.campaign')


class Main(http.Controller):

    @http.route(['/cavarosa/get_products'], type='json', auth="user", website=True)
    def get_products(self, partner_id=None, **kw):
        supplier = request.env['res.partner'].browse(int(partner_id))
        products = supplier.product_ids
        products_list = {'supplier': supplier.name, 'products': {}}
        if len(products) > 0:
            for p in products:
                products_list['products'][p.id] = {
                'name': p.name,
                'image': p.image_medium,
                'description': p.description_sale if p.description_sale else ''
                }
        return products_list

    @http.route(['/producers'], type='http', auth="public", website=True)
    def producers(self, **post):
        countries = request.env['res.district'].sudo().search([]).mapped('country_id')
        return request.website.render('website_sale_cavarosa.producers', {'countries': countries})

    @http.route(['/producer/<int:partner_id>'], type='http', auth="public", website=True)
    def producer_products(self, partner_id=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        products = partner.product_ids
        return request.website.render('website_sale_cavarosa.producer_products', {'supplier': partner, 'products': products})

    @http.route(['/country/<model("res.country"):country>'], type='http', auth="public", website=True)
    def res_country(self, country=None, **post):
        return request.website.render('website_sale_cavarosa.country', {'country': country})

    @http.route(['/district/<model("res.district"):district>'], type='http', auth="public", website=True)
    def res_district(self, district=None, **post):
        return request.website.render('website_sale_cavarosa.district', {'district': district})
