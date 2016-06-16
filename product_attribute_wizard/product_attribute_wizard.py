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

class product_attribute_wizard(models.TransientModel):
    _name = 'product.attribute.wizard'
    
    def _get_default_product_ids(self):
        ids = self.env.context.get('active_ids')
        if ids:
            return self.env['product.product'].browse(ids)
        return None
    
    product_ids = fields.Many2many(comodel_name='product.product', string='Products', relation='prod_attr_wizard_rel_product_product', required=True, default=_get_default_product_ids)
    attribute_value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='prod_attr_wizard_rel_prod_attr_val', string='Attribute Values', required=True)
    
    @api.one
    def add_product_attributes(self):
        for product in self.product_ids:
            product.attribute_value_ids = product.attribute_value_ids | self.attribute_value_ids
        
    
    
