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

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    state = fields.Selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('purchased','Purchased'),
            ('delivered', 'Delivered'),
            ('invoiced', 'Invoiced'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ])

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    @api.one
    def _compute_client_order_ref(self):
        order = self._get_order()
        return order and order.client_order_ref or ''

    client_order_ref = fields.Char(compute="_compute_client_order_ref", string="Client Order Ref")
    
class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.one
    def _compute_client_order_ref(self):
        order = self._get_order()
        _logger.warn(order)
        return order and order.client_order_ref or ''
    
    client_order_ref = fields.Char(compute="_compute_client_order_ref", string="Client Order Ref")
    
    #~ #Note: Store will not work properly. Implement search function if needed.
    #~ def _search_client_order_ref(self):
        #~ pass
    
