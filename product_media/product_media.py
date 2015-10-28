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

from openerp import fields, api, models, _
from uuid import uuid4
import logging

_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.one
    def sell_media_products(self):
        for line in self.order_line:
            if line.product_id and line.product_id.attachment_id:
                self.env['product.media.sale'].create({
                    'partner_id': self.partner_id.id,
                    'product_id': line.product_id.id,
                    'attachment_id': line.product_id.attachment_id.id,
                    'order_line_id': line.id,
                })
        return

class product_media_template(models.Model):
    _inherit = 'product.template'
    
    @api.one
    def _is_product_template(self):
        self.is_product_template = True
    
    @api.one
    def _media_sale_count(self):
        self.media_sale_count = 0
    
    @api.one
    def _media_sale_count_tmpl(self):
        self.media_sale_count_tmpl = self.env['product.media.sale'].search_count([('product_tmpl_id', '=', self.id)])
    
    attachment_id   = fields.Many2one(string='Media File', comodel_name='ir.attachment')
    media_sale_count = fields.Integer(string="Media Sales", compute='_media_sale_count')
    media_sale_count_tmpl = fields.Integer(string="Media Sales", compute='_media_sale_count_tmpl')
    #TODO: Find out if there is a way to get model name in views and scrap this field
    is_product_template = fields.Boolean(compute='_is_product_template')
        
class product_media(models.Model):
    _inherit = 'product.product'
    
    is_product_template = fields.Boolean(compute='_is_product_template')
    media_sale_count = fields.Integer(string="Media Sales", compute='_media_sale_count')
    
    @api.one
    def _is_product_template(self):
        self.is_product_template = False
    
    @api.one
    def _media_sale_count(self):
        self.media_sale_count = self.env['product.media.sale'].search_count([('product_id', '=', self.id)])

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    media_sale_count = fields.Integer(string="Media Sales", compute='_media_sale_count')
    
    @api.one
    def _media_sale_count(self):
        self.media_sale_count = self.env['product.media.sale'].search_count([('partner_id', '=', self.id)])
    
class product_media_sale(models.Model):
    _name = 'product.media.sale'
    
    name            = fields.Char(related='product_id.name')
    partner_id      = fields.Many2one(string='Customer', comodel_name='res.partner')
    product_id      = fields.Many2one(string='Product', comodel_name='product.product')
    product_tmpl_id = fields.Many2one(string="Product Template", related='product_id.product_tmpl_id')
    token           = fields.Char(string='Token', default=lambda *x: uuid4())
    attachment_id   = fields.Many2one(string='Media File', comodel_name='ir.attachment')
    order_line_id   = fields.Many2one(string='Order line', comodel_name='sale.order.line')
    image           = fields.Binary(related='product_tmpl_id.image_medium')

class install_wizard(models.TransientModel):
    _name = 'product.media.install'
    
    @api.model
    def install_module(self):
        router = self.env.ref("sale.act_router") #["workflow.activity"]
        if router.action.find('sell_media_products()') < 0:
            router.action += '\nsell_media_products()'
