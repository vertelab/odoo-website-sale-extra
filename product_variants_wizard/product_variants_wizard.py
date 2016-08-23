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
    
    def _get_default_lines(self):
        templates = self._get_default_templates()
        if templates:
            res = self.env['product.variants.wizard.line']
            for template in templates:
                for product in template.product_ids.id:
                    res = res | self.env['product.variants.wizard.line'].create({
                        'wizard_id': self.id,
                        'product_id': product,
                    })
            return res
    
    def _get_default_attribute_ids(self):
        
    
    def _get_default_template_id(self):
        templates = self._get_default_templates()
        if templates:
            return templates[0]
    
    def _get_default_template_ids(self):
        templates = self._get_default_templates()
        if templates:
            return templates[1:]
    
    def get_default_name(self):
        self._get_default_template_id().name.split(',')[0]
    
    name = fields.Char(string='Template Name', default=_get_default_name)
    product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Product Template', default=_get_default_template_id)
    product_tmpl_ids = fields.Many2many(comodel_name='product.template', relation='prod_var_wizard_rel_prod_tmpl', string='Product Templates', default=_get_default_template_ids)
    line_ids = fields.One2many(comodel_name='product.variants.wizard.line', inverse_name='wizard_id', string='Attribute Lines', default=_get_default_lines)
    price_attribute = fields.Many2one(comodel_name='product.attribute', string='Pricing Attribute', help='The attribute that will control price on the variants.')
    
    @api.multi
    def check_validity(self):
        self.ensure_one()
        #TODO: perform check
        return True
    
    @api.one
    def merge_products(self):
        if self.check_validity():
            price = self.product_tmpl_id.list_price
            #write attribute vals on products and move products to template
            for line in self.line_ids:
                line.move_product()
            #write all product.attribute.line
            for attribute in self.attribute_ids:
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
                    self.env['product.attribute.line'].create([
                        'product_tmpl_id': self.product_tmpl_id.id,
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, value_ids)],
                    ])
            #reset price for template
            self.product_tmpl_id.list_price = price
            #write product.attribute.price lines
            for line in self.line_ids:
                line.set_price(price)
            #delete unused templates
            for template in self.product_tmpl_ids:
                template.unlink()

class product_variants_wizard_line(models.TransientModel):
    _name = 'product.variants.wizard.line'
    
    def _get_default_price(self):
        return self.product_id.price
    
    def _get_default_value_ids(self):
        values = self.product_id.attribute_value_ids
        for name in self.product_id.name.split(',')[1:]:
            pass
        
    
    wizard_id = fields.Many2one(comodel_name='product.variants.wizard')
    product_id = fields.Many2one(comodel_name='product.product', string='Products', required=True)
    value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='prod_var_wizard_line_rel_prod_attr_val', string='Attribute Values')
    new_value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='prod_var_wizard_line_rel_new_prod_attr_val', string='New Attribute Values')
    price = fields.Float(string='Price', default=_get_default_price)
    
    def move_product(self):
        self.product_id.write({
            'attribute_value_ids': [(6, 0, [v.id for v in self.value_ids])]
            'product_tmpl_id': self.wizard_id.product_tmpl_id.id
        })
    
    def get_pricing_attr_value(self):
        for v in self.value_ids:
            if v.id == self.wizard_id.price_attribute:
                return v
    
    def set_price(self, tmpl_price):
        p = self.env['product.attribute.price'].search([
            ('value_id', '=', self.get_pricing_attr_value().id),
            ('product_tmpl_id', '=', self.wizard_id.product_tmpl_id.id)
        ])
        if p:
            p.write({'price_extra': self.price - tmpl_price})
        else:
            self.env['product.attribute.price'].create({
                'product_tmpl_id': self.wizard_id.product_tmpl_id.id,
                'value_id': self.get_pricing_attr_value().id,
                'price_extra': self.price - tmpl_price,
            })
    
    @api.multi
    def get_attribute_value_ids(self, attribute):
        self.ensure_one()
        ids = []
        for value in self.value_ids:
            if value.attribute_id == attribute:
                ids.append(value.id)
        return ids
    
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        product = self.env['product.product'].browse(vals['product_id'])
        #vals['price'] = product.list_price
        values = product.attribute_value_ids
        new_values = self.env['product.attribute.values']
        for name.strip() in product.name.split(',')[1:]:
            value = self.env['product.attribute.value'].search([('name', '=', name)])
            if value:
                values = values | value
            else:
                attribute = odoo.env['product.attribute'].create({'name': name})
                value = [odoo.env['product.attribute.value'].create({
                    'name': name,
                    'attribute_id': attribute.id,
                })]
                new_values = new_values | value
        if values:
            vals['value_ids'] = [(6, 0, [v.id for v in values])]
        if new_values:
            vals['new_value_ids'] = [(6, 0, [v.id for v in new_values])]
        return super(product_variants_wizard_line, self).create(vals)
