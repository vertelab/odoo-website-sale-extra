# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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

class res_partner(models.Model):
    _inherit = "res.partner"

    @api.v7
    def xname_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        return self.name_get(cr, uid, self.pool.get('res.partner').search(cr, uid, [('ref', 'ilike', name)])) + super(res_partner, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.one
    def _get_address(self):
        address_format = "%(street)s%(street2)s, %(zip)s %(city)s"

        self.invoice_address = address_format % {
            'street': self.partner_invoice_id.street or '',
            'street2': self.partner_invoice_id.street2 or '',
            'zip': self.partner_invoice_id.zip or '',
            'city': self.partner_invoice_id.city or '',}

        self.shipping_address = address_format % {
            'street': self.partner_shipping_id.street or '',
            'street2': self.partner_shipping_id.street2 or '',
            'zip': self.partner_shipping_id.zip or '',
            'city': self.partner_shipping_id.city or '',}


    invoice_address = fields.Char(compute='_get_address', string='')
    shipping_address = fields.Char(compute='_get_address', string='')
