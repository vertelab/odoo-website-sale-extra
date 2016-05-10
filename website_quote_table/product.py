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

import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    bootstrap_icon = fields.Char(string='Boostrap Icon',help="eg fa-laptop")    

class sale_order(models.Model):
    _inherit='sale.order'
    
    
    
    @api.one
    @api.depends('order_line')
    def _compute_order_line_monthly(self):
        month = self.env.ref('website_quote_table.product_uom_month')
        self.order_line_monthly = self.order_line.filtered(lambda x: x.product_id and x.product_id.uom_id == month)
        
    @api.one
    @api.depends('order_line_monthly')
    def _compute_order_line_monthly_untaxed(self):
        tot = 0.0
        for line in self.order_line_monthly:
            tot += line.price_subtotal
        self.order_line_monthly_untaxed = res
    
    @api.one
    @api.depends('order_line_monthly')
    def _compute_order_line_monthly_tax(self):
        tot = 0.0
        for line in self.order_line_monthly:
            tot += self._amount_line_tax(line)
        self.order_line_monthly_tax = res
    
    @api.one
    @api.depends('order_line_monthly_untaxed', 'order_line_monthly_tax')
    def _compute_order_line_monthly_tax(self):
        self.order_line_monthly_total = self.order_line_monthly_untaxed + self.order_line_monthly_tax
        
    
    order_line_monthly = fields.One2many('sale.order.line', compute=_compute_order_line_monthly)
    order_line_monthly_untaxed = fields.Float(compute=_compute_order_line_monthly_untaxed)
    order_line_monthly_tax = fields.Float(compute=_compute_order_line_monthly_tax)
    order_line_monthly_total = fields.Float(compute=_compute_order_line_monthly_untaxed)
