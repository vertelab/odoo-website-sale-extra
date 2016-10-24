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

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    #Field for hiding/showing email buttons
    sjm_send_email = fields.Boolean('Send Email', compute='_get_invoice_type_id')
    
    @api.one
    @api.depends('order_id', 'picking_id')
    def _get_invoice_type_id(self):
        invoice_type_id = None
        if self.order_id:
            invoice_type_id = self.order_id.invoice_type_id
        elif self.picking_id:
            invoice_type_id = self.picking_id.invoice_type_id
        if invoice_type_id and invoice_type_id.send_email:
            self.sjm_send_email = True
        else:
            self.sjm_send_email = False
