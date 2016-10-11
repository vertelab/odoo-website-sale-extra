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

class sale_journal_invoice_type(models.Model):
    _inherit = 'sale_journal.invoice.type'
    
    send_email = fields.Boolean('Send Invoice by Email')

class res_partner(models.Model):
    _inherit ='res.partner'
    
    invoice_type_id = fields.Many2one('sale_journal.invoice.type', 'Invoice Type', inverse='_set_invoice_type_id')
    
    @api.one
    def _set_invoice_type_id(self):
        for partner in self.child_ids:
            partner.invoice_type_id = self.invoice_type_id

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_type_id = fields.Many2one('sale_journal.invoice.type', 'Invoice Type', compute='_get_invoice_type_id')
    #Field for hiding/showing email buttons
    sjm_send_email = fields.Boolean('Send Email', compute='_get_invoice_type_id')
    
    @api.one
    @api.depends('order_id', 'picking_id')
    def _get_invoice_type_id(self):
        if self.order_id:
            self.invoice_type_id = self.order_id.invoice_type_id
        elif self.picking_id:
            self.invoice_type_id = self.picking_id.invoice_type_id
        if self.invoice_type_id and self.invoice_type_id.send_email:
            self.sjm_send_email = True
        else:
            self.sjm_send_email = False    

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def onchange_partner_id(self, part):
        res = super(sale_order, self).onchange_partner_id(part)
        if part:
            partner = self.env['res.partner'].search_read([('id', '=', part)], ['invoice_type_id'])
            invoice_type = partner[0].get('invoice_type_id')
            res['value']['invoice_type_id'] = invoice_type and invoice_type[0]
        return res
    
    @api.model
    def create(self, values):
        if not values.get('invoice_type_id') and values.get('partner_id'):
            partner = self.env['res.partner'].search_read([('id', '=', values.get('partner_id'))], ['invoice_type_id'])
            if partner:
                invoice_type = partner[0].get('invoice_type_id')
                values['invoice_type_id'] = invoice_type and invoice_type[0]
        return super(sale_order, self).create(values)
