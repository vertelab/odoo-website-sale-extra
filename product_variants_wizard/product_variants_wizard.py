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
from openerp.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class product_variants_wizard(models.TransientModel):
    _name = 'product.variants.wizard'
    
    @api.model
    def _get_default_templates(self):
        ids = self.env.context.get('active_ids')
        if ids:
            return self.env['product.template'].browse(ids).sorted(lambda r: r.product_variant_count, True)
        return self.env['product.template'].browse()
    
    def _get_default_lines(self):
        templates = self._get_default_templates()
        if templates:
            res = []
            for template in templates:
                for product in template.product_variant_ids:
                    value = self.env['product.attribute.value']
                    res.append({
                        'product_id': product.id,
                        'value_ids': self._get_default_value_ids(product),
                        'price': product.lst_price,
                    })
            return [(0, 0, vals) for vals in res]
        return self.env['product.variants.wizard.line'].browse()
    
    def _get_default_template_id(self):
        templates = self._get_default_templates()
        if templates:
            return templates[0]
        return templates
    
    def _get_default_template_ids(self):
        templates = self._get_default_templates()
        if templates:
            return templates[1:]
        return templates
    
    def _get_default_name(self):
        template = self._get_default_template_id()
        if template:
            return template.name.split(',')[0]
        return template
    
    def _default_price_attribute(self):
        #TODO: Look at price lines to find currently used price attribute
        templates = self._get_default_templates()
        if templates:
            for template in templates:
                for product in template.product_variant_ids:
                    for value in product.attribute_value_ids:
                        if value.attribute_id:
                            return value.attribute_id
        return self.env['product.attribute'].browse()
    
    name = fields.Char(string='Template Name', default=_get_default_name, required=True)
    product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Main Template', default=_get_default_template_id, required=True)
    product_tmpl_ids = fields.Many2many(comodel_name='product.template', relation='prod_var_wizard_rel_prod_tmpl', string='Product Templates', default=_get_default_template_ids)
    line_ids = fields.One2many(comodel_name='product.variants.wizard.line', inverse_name='wizard_id', string='Variant Lines', default=_get_default_lines)
    base_price = fields.Float(string="Base Price", compute="_get_base_price")
    attribute_ids = fields.Many2many(comodel_name='product.attribute', string='Attributes', compute="_get_product_attributes", help='Lists all attributes of the product values on the Attribute Lines below.')
    price_attribute = fields.Many2one(comodel_name='product.attribute', string='Pricing Attribute', default=_default_price_attribute, required=True, help='This attribute will be tied to product prices.')
    
    @api.model
    def _get_default_value_ids(self, product, attribute=None):
        values = product.attribute_value_ids
        res = []
        for name in product.name.split(',')[1:]:
            name = name.strip()
            if not attribute:
                value = self.env['product.attribute.value'].search([('name', '=', name)])
            else:
                value = self.env['product.attribute.value'].search([('name', '=', name), ('attribute_id', '=', attribute.id)])
            if value:
                values |= value
        if values:
            res += [(6, 0, [v.id for v in values])]
        return res
    
    @api.one
    @api.depends('line_ids', 'line_ids.value_ids', 'line_ids.value_ids.attribute_id')
    def _get_product_attributes(self):
        attributes = self.env['product.attribute'].browse()
        for line in self.line_ids:
            for value in line.value_ids:
                attributes |= value.attribute_id
        self.attribute_ids = attributes
    
    @api.one
    @api.depends('line_ids', 'line_ids.price')
    def _get_base_price(self):
        price = None
        for line in self.line_ids:
            if not price:
                price = line.price
            elif line.price < price:
                price = line.price
        self.base_price = price
    
    @api.multi
    def check_validity(self):
        self.ensure_one()
        if not self.price_attribute:
            raise Warning("You must set the Pricing Attribute.")
        for line in self.line_ids:
            attributes = self.attribute_ids
            for value in line.value_ids:
                if value.attribute_id not in attributes:
                    raise Warning("%s has multiple values for attribute %s." % (line.product_id.name, value.attribute_id.name))
                attributes -= value.attribute_id
            if len(attributes) > 0:
                raise Warning("%s is missing values for attributes %s." % (line.product_id.name, [a.name for a in attributes]))
        return True
    
    @api.one
    def merge_products(self):
        if self.check_validity():
            #write attribute vals on products and move products to template
            for line in self.line_ids:
                line.move_product()
            #write all product.attribute.line
            for attribute in self.attribute_ids:
                #Get all values used for this attribute
                value_ids = []
                for line in self.line_ids:
                    value_ids += line.get_attribute_value_ids(attribute)
                value_ids = list(set(value_ids))
                line = self.env['product.attribute.line'].search([
                    ('product_tmpl_id', '=', self.product_tmpl_id.id),
                    ('attribute_id', '=', attribute.id),
                ])
                if line:
                    line.write({'value_ids': [(6, 0, value_ids)]})
                else:
                    self.product_tmpl_id.write({
                        'attribute_line_ids': [(0, 0, {
                            'attribute_id': attribute.id,
                            'value_ids': [(6, 0, value_ids)],
                        })],
                    })
            #reset price for template
            self.product_tmpl_id.list_price = self.base_price
            #reset variant prices
            for line in self.line_ids:
                line.set_price()
            #Move BOMs
            for template in self.product_tmpl_ids:
                for bom in template.bom_ids:
                    bom.write({'product_tmpl_id': self.product_tmpl_id.id})
                #delete unused templates
                template.unlink()
            new_products = self.product_tmpl_id.product_variant_ids
            #New products created?
            for line in self.line_ids:
                new_products -= line.product_id

class product_variants_wizard_line(models.TransientModel):
    _name = 'product.variants.wizard.line'
    
    wizard_id = fields.Many2one(comodel_name='product.variants.wizard')
    product_id = fields.Many2one(comodel_name='product.product', string='Products', required=True)
    value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='prod_var_wizard_line_rel_prod_attr_val', string='Attribute Values')
    price = fields.Float(string='Price')
    
    @api.multi
    def get_pricing_attr_value(self):
        for value in self.value_ids:
            if value.attribute_id == self.wizard_id.price_attribute:
                return value
    
    def move_product(self):
        template = self.product_id.product_tmpl_id
        self.product_id.write({
            'name': self.wizard_id.name,
            'attribute_value_ids': [(6, 0, [v.id for v in self.value_ids])],
            'product_tmpl_id': self.wizard_id.product_tmpl_id.id
        })
    
    def set_price(self):
        price_extra = self.price - self.wizard_id.base_price
        value = self.get_pricing_attr_value()
        p = self.env['product.attribute.price'].search([
            ('value_id', '=', value.id),
            ('product_tmpl_id', '=', self.wizard_id.product_tmpl_id.id)
        ])
        if p:
            p.write({'price_extra': price_extra})
        else:
            self.env['product.attribute.price'].create({
                'product_tmpl_id': self.wizard_id.product_tmpl_id.id,
                'value_id': value.id,
                'price_extra': price_extra,
            })
    
    @api.multi
    def get_attribute_value_ids(self, attribute):
        self.ensure_one()
        ids = []
        for value in self.value_ids:
            if value.attribute_id == attribute:
                ids.append(value.id)
        return ids
    
