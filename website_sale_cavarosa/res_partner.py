# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
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

    campaign_ids = fields.Many2many(string='Campaigns', comodel_name='crm.tracking.campaign')
    seller_ids = fields.One2many(string='Suppliers', comodel_name='product.supplierinfo', inverse_name='name')
    @api.one
    def _product_ids(self):
        self.product_ids = [(6, 0, [s.product_tmpl_id.id for s in self.seller_ids])]
    product_ids = fields.Many2many(string='Products', comodel_name='product.template', compute='_product_ids')


class product_snippet(http.Controller):

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
