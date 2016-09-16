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

class product_template(models.Model):
    _inherit = 'product.template'
    
    product_customer_code = fields.Char('Customer Product Code', compute='_get_product_customer_code_dummy', search='_search_product_customer_code')
    
    def _get_product_customer_code_dummy(self):
        self.product_customer_code = ''
    
    def _search_product_customer_code(self, operator, value):
        product_ids = []
        for line in self.env['product.customer.code'].search_read([('product_code', operator, value)], ['product_id']):
            _logger.warn(line)
            product_ids.append(line['product_id'][0])
        product_ids = list(set(product_ids))
        if self._name == 'product.product':
            return [('id', 'in', product_ids)]
        elif self._name == 'product.template':
            return [('product_variant_ids', 'in', product_ids)]
    
    
