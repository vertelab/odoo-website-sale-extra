# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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

from openerp import fields, api, models, _, http
from openerp.http import request
from uuid import uuid4
from wand.image import Image

import logging

_logger = logging.getLogger(__name__)

class ProductPhotoDownload(http.Controller):
    
    @http.route('/product_photo/download/<int:sale>', type='http', auth="user", website=True)
    def download(self, sale=0, **post):
        user = request.env['res.users'].browse(request.uid)
        sale = request.env['product.media.sale'].sudo().browse(sale)
        if not (user.partner_id and user.partner_id == sale.partner_id):
            return "You do not have access rights to this document"
        recipe = sale.product_id.attribute_value_ids[0].im_recipe_id
        return recipe.sudo().send_file(http,field='media_file',model='product.product',id=sale.product_id.id)

class product_media_sale(models.Model):
    _inherit = 'product.media.sale'
    
    license = fields.Many2one(comodel_name='product.photo.license', string='License')

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    license = fields.Many2one(comodel_name='product.photo.license', string='License')
    
    @api.multi
    def product_id_change(self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = super(sale_order_line, self).product_id_change(pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag)
        if product:
            product = self.env['product.product'].browse(product)
            if product.media_type == 'photo' and product.license:
                res['value']['license'] = product.license.id
        return res
        
class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def sell_media_photo_product(self, values, line):
        values.update({
            'license': line.license.id,
        })
        return values

class product_media_template(models.Model):
    _inherit = 'product.template'
    
    author = fields.Many2one(comodel_name='res.partner', string='Photographer')
    license = fields.Many2one(comodel_name='product.photo.license', string='License')
    model = fields.Char('Model')
    
    @api.onchange('media_type')
    def _onchange_media_type(self):
        if self.media_type == 'photo':
            attr = self.env.ref('product_photo.image_attributes')
            val_s = self.env.ref('product_photo.image_attr_small')
            val_m = self.env.ref('product_photo.image_attr_medium')
            val_l = self.env.ref('product_photo.image_attr_large')
            self.attribute_line_ids = [(0, 0, {
                'attribute_id': attr.id,
                'value_ids':   [(4, val_s.id, 0),
                                (4, val_m.id, 0),
                                (4, val_l.id, 0)],
            })]
    @api.model
    def _get_media_types(self):
        res = super(product_media_template, self)._get_media_types()
        res.append(('photo', 'Photo'))
        return res
        
    @api.model
    def create(self, vals):
        _logger.warn('create: %s' % vals)
        if vals.get('media_type') == 'photo':
            photo = vals.get('media_file')
            if photo:
                recipe = self.env.ref('product_photo.thumbnail_recipe')
                vals['image_medium'] = recipe.run(Image(blob=photo.decode('base64'))).make_blob().encode('base64')
        return super(product_media_template, self).create(vals)

    @api.multi
    def write(self, vals):
        _logger.warn('write: %s' % vals)
        if vals.get('media_type') != 'photo':
            for record in self:
                if record.media_type != 'photo':
                    return super(product_media_template, self).write(vals)
        photo = vals.get('media_file')
        if photo:
            recipe = self.env.ref('product_photo.thumbnail_recipe')
            vals['image'] = recipe.run(Image(blob=photo.decode('base64'))).make_blob().encode('base64')
        return super(product_media_template, self).write(vals)

class product_attribute_value(models.Model):
    _inherit = 'product.attribute.value'
    
    im_recipe_id = fields.Many2one(string="Imagemagick Recipe", comodel_name="image.recipe")

class product_license(models.Model):
    _name = 'product.photo.license'
    
    name                = fields.Char('Name')
    website_description = fields.Html('Description')
