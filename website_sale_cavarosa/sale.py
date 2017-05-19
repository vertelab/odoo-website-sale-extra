# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale
import logging
_logger = logging.getLogger(__name__)

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    partner = fields.Char(related='order_id.partner_id.name')
    street = fields.Char(related='order_id.partner_id.street')
    zip = fields.Char(related='order_id.partner_id.zip')
    city = fields.Char(related='order_id.partner_id.city')
    product_name = fields.Char(related='product_id.name')
    unit_qty = fields.Integer(compute='_unit_qty')
    shipping_name = fields.Char(related='order_id.partner_shipping_id.name')
    shipping_street = fields.Char(related='order_id.partner_shipping_id.street')
    shipping_zip = fields.Char(related='order_id.partner_shipping_id.zip')
    shipping_city = fields.Char(related='order_id.partner_shipping_id.city')
    carrier_info = fields.Char(compute='_carrier_info')
    order_name = fields.Char(related='order_id.name')
    mobile = fields.Char(related='order_id.partner_id.mobile')
    campaign_id = fields.Many2one(related='order_id.campaign_id', comodel_name='crm.tracking.campaign', store=True)
    supplier_id = fields.Many2one(compute='_supplier_id', comodel_name='res.partner', store=True)

    @api.one
    def _supplier_id(self):
        self.supplier_id = self.procurement_ids.mapped('purchase_id.partner_id')[0]

    @api.one
    def _unit_qty(self):
        self.unit_qty = int(self.product_id.uom_id.factor_inv) if self.product_id.uom_id.uom_type == 'bigger' else 1

    @api.one
    def _carrier_info(self):
        if self.order_id.carrier_id == self.env.ref('cavarosa_delivery.delivery_carrier'): #cavarosafack
            self.carrier_info = self.order_id.carrier_id.name + ': ' + self.order_id.cavarosa_box
        elif self.order_id.carrier_id.pickup_location: #utlämningsställe
            self.carrier_info = self.order_id.carrier_id.name + ': ' + self.order_id.partner_shipping_id.name
        else:   #hemleverans
            self.carrier_info = self.order_id.carrier_id.name
