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
from openerp.exceptions import except_orm, Warning, RedirectWarning
import urllib2
import base64
from cStringIO import StringIO

import logging
_logger = logging.getLogger(__name__)

try:
    import unicodecsv as csv
except:
    _logger.info('Missing unicodecsv. sudo pip install unicodecsv')

class CavarosaImport(models.TransientModel):
    _name = 'sale.cavarosa.import.wizard'

    commerce_product = fields.Binary('commerce_product.csv', required=True)
    produktvisningar = fields.Binary('Produktvisningar', required=True)
    suppliers = fields.Binary('Leverantörer', required=True)
    districts = fields.Binary('Distrikt', required=True)


    @api.one
    def import_files(self):
        districts = {}
        for r in self.env['res.district'].search([]):
            districts[r.name] = r
        suppliers = {}
        for r in self.env['res.partner'].search([('supplier', '=', True)]):
            suppliers[r.name] = r
        products = {}
        #~ for r in self.env['product.template'].search():
            #~ products[r.name] = r
        ignore = ('10', '18', '57')
        f = csv.reader(StringIO(base64.b64decode(self.districts)))
        for row in f:
            if row[0]:
                _logger.warn(row)
                image = self.download_image(row[1])
                vals = {
                    'name': row[0],
                    'country_id': self.find_country(row[2]),
                    'website_description': (image and '<img src="data:image/png;base64,%s" />' % image) or '',
                }
                if not vals['name'] in districts:
                    districts[row[0]] = self.env['res.district'].create(vals)
                else:
                    districts[vals['name']].write(vals)

        f = csv.reader(StringIO(base64.b64decode(self.suppliers)))
        for row in f:
            if row[0]:
                district = districts.get(row[1])
                if not district:
                    district = districts[row[1]] = districts[row[0]] = self.env['res.district'].create({
                        'name': row[0],
                    })
                vals = {
                    'customer': False,
                    'supplier': True,
                    'name': row[0],
                    'district_id': district.id,
                    'image': self.download_image(row[2]),
                    'country_id': self.find_country(row[3]),
                    'comment': row[4],
                }
                if not vals['name'] in suppliers:
                    suppliers[row[0]] = self.env['res.partner'].create(vals)
                else:
                    suppliers[vals['name']].write(vals)

        f = csv.DictReader(StringIO(base64.b64decode(self.commerce_product)))
        for row in f:
            if row[u'Product ID'] not in ignore:
                products[row[u'Product ID']] = {
                    'list_price': float(row.get(u'Pris', '0').split(' ')[0]) / 100,
                    'name': row[u'Titel'],
                    'image': self.download_image(row[u'Bild']),
                    'seller_ids': [(0, 0, {'name': suppliers[row[u'Leverantör']].id})] if row[u'Leverantör'] else False,
                }

        f = csv.DictReader(StringIO(base64.b64decode(self.produktvisningar)))
        for row in f:
            if row[u'Produkt (vara)'] and (row[u'Produkt (vara)'] not in ignore):
                uom = self.find_uom(row[u'Typ'].split(' ')[1])
                products[row[u'Produkt (vara)']].update({
                    'description_sale': row[u'Beskrivning'],
                    'uom_id': uom.id,
                    'list_price': uom.factor_inv * products[row[u'Produkt (vara)']]['list_price'],
                })

        for id in products.keys():
            self.set_external_id(self.env['product.template'].create(products[id]), 'commerce_product_%s' % id)


    @api.model
    def find_uom(self, name):
        if name == '1-pack':
            name = 'st'
        uom = self.env['product.uom'].search([('name', '=', name)])
        if not uom:
            raise Warning("Couldn't find a unit of measure for %s." % name)
        return uom

    @api.model
    def set_external_id(self, record, name):
        self.env['ir.model.data'].create({
            'name': name,
            'model': record._name,
            'module': '__cavarosa_import__',
            'res_id': record.id,
        })

    @api.model
    def find_country(self, name):
        country = self.env['res.country'].search([('name', '=', name)])
        if not country and len(country) == 1:
            raise Warning("Couldn't find a match for country %s" % name)
        return country.id

    @api.model
    def download_image(self, image_name):
        #TODO: Use Paramiko SFTP instead
        image = ''
        if image_name:
            url = 'http://www.cavarosawine.se/sites/default/files/cavarosawine_se/%s' % image_name.split(' (')[0].strip()
            _logger.warn(url)
            try:
                image = base64.b64encode(urllib2.urlopen(url).read())
            except:
                _logger.warn("Couldn't get %s." % url)
        return image
