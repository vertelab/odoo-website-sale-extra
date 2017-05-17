# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
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
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
import base64
_logger = logging.getLogger(__name__)

from cStringIO import StringIO
try:
    import unicodecsv as csv
except:
    _logger.info("sale_order_line_import requires unicodecsv")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    invoice_number = fields.Char('Invoice Number')
    invoice_date = fields.Date('Invoice Date')
    delivery_city = fields.Char('Delivery City')
    delivery_name = fields.Char('Delivery Name')
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    serial_number = fields.Char('Serial Number')
    invoice_number = fields.Char(related='order_id.invoice_number')
    invoice_date = fields.Date(related='order_id.invoice_date')
    delivery_city = fields.Char(related='order_id.delivery_city')
    delivery_name = fields.Char(related='order_id.delivery_name')

class OrderLineImport(models.TransientModel):
    _name = 'sale.order.line.import.wizard'
    
    data = fields.Binary('CSV File', required=True)
    
    @api.one
    def import_file(self):
        csv_data = csv.DictReader(StringIO(base64.b64decode(self.data)), encoding='utf-8')
        customers = {}
        orders = {}
        
        for row in csv_data:
            customer = customers.get(row['Kundnummer'])
            if not customer:
                customer = self.env['res.partner'].search([('customer_no', '=', row['Kundnummer']), ('parent_id', '=', False)])
                customers[customer.customer_no] = customer
            if not customer:
                raise Warning("Couldn't find customer with number %s." % row['Kundnummer'])
            order = orders.get(row['Ordernummer'])
            if not order:
                order = self.env['sale.order'].create({
                    'name': row['Ordernummer'],
                    'partner_id': customer.id,
                    'invoice_number': row['Fakturanummer'],
                    'invoice_date': row['Fakturadatum'],
                    'delivery_city': row['Ort'],
                    'delivery_name': row['Kundnamn'],
                    'state': 'done',
                })
                if order.pricelist_id.currency_id.name != row['Valutakod']:
                    order.pricelist_id = self.env['product.pricelist'].search([('currency_id.name', '=', row['Valutakod'])], limit=1)
                orders[order.name] = order
            
            product = self.env['product.product'].search([('default_code', '=', row['Artikelnummer'])])
            net_sum = float(row['Nettoradsumma'])
            qty = float(row['Antal'])
            price = float(row['Nettopris/st'])
            discount = 100.0 * (1.0 - net_sum / (qty * price))
            if discount < 0.01:
                discount = 0.0
            self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': product and product.id or False,
                'name': '[%s] %s%s' % (row['Artikelnummer'], row['Benamning'], (' (%s)' % row['Kommentar']) if row['Kommentar'] else ''),
                'product_uom_qty': qty,
                'price_unit': price,
                'discount': discount,
                'serial_number': row['Serienummer'],
            })
            
            #Fakturanummer	Fakturadatum	Ordernummer	Kundnummer	Kundnamn	Ort	Artikelnummer	Benämning	Kommentar	Serienummer	Antal	Nettopris/st	Nettoradsumma	Valutakod

            #name            orderreferens (ordernummer)
            #customer_no     kundnummer (slå upp lägg på currency_id från valutakoden, )
            #invoice_number  fakturanummer (nytt fält)
            #delivery_city   leveransort (nytt fält)
            #delivery_name   leveransnamn (nytt fält)
            #invoice_date    fakturadatum (orderraddatum + ev period)
            #name            valutakoden (orderhuvud)
            
            #Lines
            #default_code    artikelnummer (slå upp, saknas så använd bara benämningen med artnummer som prefix)
            #name            artikelbenämning
            #name            kommentar (slå samman med artikelbenämning)
            #antal
            #nettopris
            #nettosumma
            #serienummer (nyttfält)
