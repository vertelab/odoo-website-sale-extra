# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
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

from openerp import api, models, fields, _

import logging
_logger = logging.getLogger(__name__)

class product_variants_wizard(models.TransientModel):
    _name = 'product.variants.wizard'
    
    @api.model
    def _get_default_templates(self):
        ids = self.env.context.get('active_ids')
        if ids:
            return self.env['product.template'].browse(ids).sorted(lambda r: r.list_price)
    
    def _get_default_product_ids(self):
        templates = self._get_default_templates()
        if templates:
            res = self.env['product.product']
            for template in templates:
                res = res | template.product_ids
            return res
    
    def _get_default_template_id(self):
        templates = self._get_default_templates()
        if templates:
            return templates[0]
    
    name = fields.Char(string='Template Name')
    product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Product Template', default=_get_default_template_id)
    product_ids = fields.Many2many(comodel_name='product.product', string='Products', relation='prod_var_wizard_rel_product_product', required=True, default=_get_default_product_ids)
    line_ids = fields.One2many(comodel_name='product.variants.wizard.line', inverse_name='wizard_id', string='Attribute Lines')
    
    @api.one
    def merge_products(self):
        if len(self.product_ids) > 1:
            price = self.product_ids[0].list_price
            #write attribute vals on product
            #move product to template
            #repeat for all products
            #write all product.attribute.line
            #reset price for template
            #write product.attribute.price lines
            #delete unused templates
            for product in self.product_ids[1:]:
                product.attribute_value_ids = product.attribute_value_ids | self.attribute_value_ids
            
            for t in variant_prices:
                self.env['product.attribute.price'].create({
                    'product_tmpl_id': template_id,
                    'value_id': t[0],
                    'price_extra': t[1] - lprice,
                })

class product_variants_wizard_line(models.TransientModel):
    _name = 'product.variants.wizard.line'
    
    wizard_id = fields.Many2one(comodel_name='product.variants.wizard')
    attribute_id = fields.Many2one(comodel_name='product.attribute', string="Attribute")
    value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='prod_var_wizard_line_rel_prod_attr_val', string='Attribute Values', required=True)
    
    
    
            
    
    
