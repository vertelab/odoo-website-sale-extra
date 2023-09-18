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
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'
    website_description = fields.Html(string="Website Description")

    def _unit_price(self):
        for price in self:
            if price.sudo().uom_id.factor:
                price.unit_price = price.list_price * price.sudo().uom_id.factor
            elif price.sudo().uom_id.factor_inv:
                price.unit_price = price.list_price / price.sudo().uom_id.factor_inv
            else:
                price.unit_price = price.list_price
    unit_price = fields.Monetary(string='Unit Price', digits=(16, 0), compute='_unit_price')
    
    def _seller_id(self):
        for seller in self:
            seller.seller_id = seller.seller_ids[0].name if len(seller.seller_ids) > 0 else None
    seller_id = fields.Many2one(comodel_name='res.partner', compute='_seller_id')

    def _campaign_product(self):
        for camp_prod in self:
            campaign = camp_prod.env['website'].current_campaign()
            if campaign and (camp_prod in campaign[0].campaign_product_ids.mapped('product_id')):
                camp_prod.campaign_product = True
            else:
                camp_prod.campaign_product = False
    campaign_product = fields.Boolean(string='Is Campaign Product', compute='_campaign_product')
    # website_short_desc = fields.Text(string='Website Short Desc', help='This description only shows in product grid view')
    website_short_description = fields.Text(string='Website Short Description',
                                            help='This description only shows in product grid view')

    @api.model
    def products_list(self, domain, order, row):
        domain += [('website_published', '=', True)]
        products = self.env['product.template'].sudo().search(domain, order=order)
        products_list = []
        products_tmp = []
        for i, product in enumerate(list(products)):
            products_tmp.append(product)
            if (i+1)%row == 0:
                products_list.append(products_tmp)
                products_tmp = []
        return products_list
