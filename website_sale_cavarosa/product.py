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
import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    def get_unit_price(self):
        if self.uom_id.factor:
            self.unit_price = self.list_price * self.uom_id.factor
        elif self.uom_id.factor_inv:
            self.unit_price = self.list_price / self.uom_id.factor_inv
        else:
            self.unit_price = self.list_price
    unit_price = fields.Float(string='Unit Price', digits=(16, 0), compute='get_unit_price')
