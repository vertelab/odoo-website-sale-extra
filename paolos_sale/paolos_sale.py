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

class purchase_order(models.Model):
    _inherit = 'purchase.order'
    
    @api.multi
    def _get_sale_orders(self):
        self.ensure_one()
        order_names = self.origin.split(', ')
        return self.env['sale.order'].search([('name', 'in', order_names)])
    
    @api.multi
    def wkf_approve_order(self):
        res = super(purchase_order, self).wkf_approve_order()
        for order in self:
            for so in self._get_sale_orders():
                purchased = True
                for po in self.search([('origin', 'like', '%%%s%%' % so.name)]):
                    if po.state not in ['approved', 'done']:
                        purchased = False
                if purchased and so.state in ['progress']:
                    so.state = 'purchased'
                    so.signal_workflow('set_as_purchased')
        return res

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    @api.one
    def _compute_client_order_ref(self):
        order = self._get_order()
        return order and order.client_order_ref or ''

    client_order_ref = fields.Char(compute="_compute_client_order_ref", string="Client Order Ref")
    
    @api.multi
    def do_transfer(self):
        _logger.warn('\n\ndo_transfer')
        res = super(stock_picking, self).do_transfer()
        for picking in self:
            if picking.group_id:
                for so in self.env['sale.order'].search([('procurement_group_id', '=', picking.group_id.id)]):
                    _logger.warn('%s, %s' % (so.name, so.state))
                    delivered = True
                    for p in so.picking_ids:
                        _logger.warn('%s, %s' %(p.name, p.state))
                        if p.state not in ['done']:
                            delivered = False
                    if delivered and so.state in ['progress', 'purchased']:
                        so.state = 'delivered'
                        so.signal_workflow('set_as_delivered')
        return res

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
    
    @api.multi
    def invoice_validate(self):
        _logger.warn('\n\ninvoice_validate')
        res = super(account_invoice, self).invoice_validate()
        for invoice in self:
            _logger.warn('%s, %s' %(invoice.name, invoice.state))
            for so in self.env['sale.order'].search([('invoice_ids', '=', invoice.id)]):
                invoiced = True
                for i in so.invoice_ids:
                    _logger.warn('%s, %s' %(i.name, i.state))
                    if i.state not in ['open', 'paid']:
                        invoiced = False
                if invoiced and so.state in ['progress', 'purchased', 'delivered']:
                    _logger.warn('invoiced')
                    so.state = 'invoiced'
                    so.signal_workflow('set_as_invoiced')
                _logger.warn('%s, %s' %(so.name, so.state))
        return res
