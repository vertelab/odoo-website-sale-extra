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

class product_product(models.Model):
    _inherit ='product.product'

    @api.v7
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        values = name.split(',')
        ids = set(self.pool.get('product.product').search(cr, uid, [('name','ilike',values[0].strip()), ('sale_ok', '=', True)], context=context))
        if len(values) > 1:
            attributes = values[1:]
            for attr in attributes:
                ids = ids & set(self.pool.get('product.product').search(cr, uid, [('attribute_value_ids.name','ilike',attr.strip())], context=context))

        return list(set(self.name_get(cr, uid, ids)) | set(super(product_product, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)))
