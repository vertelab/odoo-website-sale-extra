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
import base64
# from cStringIO import StringIO

import logging

_logger = logging.getLogger(__name__)

try:
    import unicodecsv as csv
except:
    _logger.info('Missing unicodecsv. sudo pip install unicodecsv')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    drupal_parent_ids = fields.Many2many(string='Drupal Parents', comodel_name='res.partner',
                                         relation='drupal_partner_rel_partner', column1='child_id', column2='parent_id')


class CavarosaImport(models.TransientModel):
    _name = 'sale.cavarosa.import.wizard'

    commerce_product = fields.Binary('commerce_product.csv')
    produktvisningar = fields.Binary('Produktvisningar')
    suppliers = fields.Binary('Leverantörer')
    districts = fields.Binary('Distrikt')
    users = fields.Binary('Users')
    order_lines = fields.Binary('Order Lines')
    customers = fields.Binary('Customers')
    username = fields.Char(string='Username', required=True, help="Your username on wiggum.vertel.se")
    password = fields.Char(string='Password', required=True, help="Your password on wiggum.vertel.se")

    def import_files(self):
        for importf in self:

            try:
                # ~ if True:
                districts = {}
                for r in importf.env['res.district'].search([]):
                    districts[r.name] = r
                suppliers = {}
                for r in importf.env['res.partner'].search([('supplier', '=', True)]):
                    suppliers[r.name] = r
                products = {}
                # ~ for r in self.env['product.template'].search():
                # ~ products[r.name] = r
                users = {}
                customers = {}
                ignore = ('10', '18', '57')
                users_ignore = ('1730', '1763', '1547', '457', '1769', '1515', '1721')

                # Import districts
                if importf.districts:
                    f = csv.reader(StringIO(base64.b64decode(importf.districts)))
                    for row in f:
                        if row[0]:
                            _logger.warn(row)
                            image = importf.download_image(row[1])
                            vals = {
                                'name': row[0],
                                'country_id': importf.find_country(row[2]),
                                'website_description': (
                                                                   image and '<img src="data:image/png;base64,%s" />' % image) or '',
                            }
                            if not vals['name'] in districts:
                                districts[row[0]] = importf.env['res.district'].create(vals)
                            else:
                                districts[vals['name']].write(vals)

                    # Import suppliers
                    if importf.suppliers:
                        f = csv.reader(StringIO(base64.b64decode(importf.suppliers)))
                        for row in f:
                            if row[0]:
                                district = districts.get(row[1])
                                if not district:
                                    district = districts[row[1]] = importf.env['res.district'].create({
                                        'name': row[1],
                                    })
                                vals = {
                                    'customer': False,
                                    'supplier': True,
                                    'name': row[0],
                                    'district_id': district.id,
                                    'image': importf.download_image(row[2], '/var/lib/drupal7/files/cavarosawine_se/'),
                                    'country_id': importf.find_country(row[3]),
                                    'comment': row[4],
                                }
                                if not vals['name'] in suppliers:
                                    suppliers[vals['name']] = importf.env['res.partner'].create(vals)
                                else:
                                    suppliers[vals['name']].write(vals)

                # Import products
                if importf.commerce_product and importf.produktvisningar:
                    f = csv.DictReader(StringIO(base64.b64decode(importf.commerce_product)))
                    for row in f:
                        if row[u'Product ID'] not in ignore:
                            products[row[u'Product ID']] = {
                                'list_price': float(row.get(u'Pris', '0').split(' ')[0]) / 100,
                                'name': row[u'Titel'],
                                'image': importf.download_image(row[u'Bild']),
                                'seller_ids': [(0, 0, {'name': suppliers[row[u'Leverantör']].id})] if row[
                                    u'Leverantör'] else False,
                            }
                    f = csv.DictReader(StringIO(base64.b64decode(importf.produktvisningar)))
                    for row in f:
                        if row[u'Produkt (vara)'] and (row[u'Produkt (vara)'] not in ignore):
                            uom = importf.find_uom(row[u'Typ'].split(' ')[1])
                            products[row[u'Produkt (vara)']].update({
                                'description_sale': row[u'Beskrivning'],
                                'uom_id': uom.id,
                                'list_price': uom.factor_inv * products[row[u'Produkt (vara)']]['list_price'],
                            })

                    for id in products.keys():
                        xml_id = 'commerce_product_%s' % id
                        template = importf.env['ir.model.data'].xmlid_to_object('__cavarosa_import__.%s' % xml_id)
                        if template:
                            template.write(products[id])
                        else:
                            importf.set_external_id(importf.env['product.template'].create(products[id]), xml_id)

                # Import customers
                if importf.customers:
                    f = csv.DictReader(StringIO(base64.b64decode(importf.customers)))
                    for row in f:
                        exid = 'drupal_customer_profile_id_%s' % row[u'Profil-ID']
                        if row[u'Typ'] == 'Betalningsinformation':
                            country = importf.find_country(row[u'Address - Land'])
                            customers[exid] = importf.env['res.partner'].create({
                                'customer': True,
                                'name': row[u'Address - Fullständigt namn'],
                                'street': row[u'Address - Huvudgata (till exempel gatuadress)'],
                                'street2': row[u'Address - Fastighet (till exempel lägenhets/svitnummer)'],
                                'zip': row[u'Address - Postnummer'],
                                'city': row[u'Address - Ort (till exempel stad)'],
                                'state_id': importf.find_state(
                                    row[u'Address - Administrativt område (till exempel stat/provins)'], country),
                                'country_id': country,
                                'phone': row[u'Telefon'],
                                'comment': row[u'Övriga upplysningar /Meddelanden'],
                            })
                            importf.set_external_id(customers[exid], exid)
                        elif row[u'Typ'] == 'Shipping information':
                            country = importf.find_country(row[u'Address - Land'])
                            customers[exid] = importf.env['res.partner'].create({
                                'type': 'delivery',
                                'name': row[u'Address - Fullständigt namn'],
                                'street': row[u'Address - Huvudgata (till exempel gatuadress)'],
                                'street2': row[u'Address - Fastighet (till exempel lägenhets/svitnummer)'],
                                'zip': row[u'Address - Postnummer'],
                                'city': row[u'Address - Ort (till exempel stad)'],
                                'state_id': importf.find_state(
                                    row[u'Address - Administrativt område (till exempel stat/provins)'], country),
                                'country_id': country,
                                'phone': row[u'Telefon'],
                                'comment': row[u'Övriga upplysningar /Meddelanden'],
                            })
                            importf.set_external_id(customers[exid], exid)
                        else:
                            raise Warning('Unknown type: %s' % row[u'Typ'])

                # Import users
                delivery_users = []
                unknown_users = []
                if importf.users:
                    portal = importf.env['ir.model.data'].get_object('base', 'group_portal')
                    f = csv.DictReader(StringIO(base64.b64decode(importf.users)))
                    for row in f:
                        exid = 'drupal_uid_%s' % row[u'Uid']
                        partner = customers.get('drupal_customer_profile_id_%s' % row[u'Profil-ID'])
                        if partner and partner.type != 'delivery':
                            # Ignore problem cases
                            if row[u'Uid'] not in users_ignore:
                                if exid in users:
                                    if partner.parent_id:
                                        _logger.warn('Partner %s tillhörde %s. Flyttad till %s' % (
                                        partner.id, partner.parent_id.id, users[exid].partner_id.id))
                                    partner.parent_id = users[exid].partner_id
                                else:
                                    users[exid] = importf.env['res.users'].with_context(
                                        {'no_reset_password': True}).create({
                                        'partner_id': partner.id,
                                        'name': partner.name,
                                        'login': row[u'Namn'],
                                        'email': row[u'E-post'],
                                        'create_date': row[u'Skapad datum'] or False,
                                        'login_date': row[u'Senaste inloggning'] or False,
                                        'groups_id': [(6, 0, [portal.id])],
                                    })
                                    importf.set_external_id(users[exid], exid)
                        if partner:
                            # Save delivery adresses for later
                            delivery_users.append({
                                'exid': exid,
                                'partner_id': partner,
                                'name': partner.name,
                                'login': row[u'Namn'],
                                'email': row[u'E-post'],
                                'create_date': row[u'Skapad datum'] or False,
                                'login_date': row[u'Senaste inloggning'] or False,
                                'groups_id': [(6, 0, [portal.id])],
                            })
                        else:
                            # Save users without customers for later.
                            unknown_users.append({
                                'exid': exid,
                                'name': row[u'Namn'],
                                'login': row[u'Namn'],
                                'email': row[u'E-post'],
                                'create_date': row[u'Skapad datum'] or False,
                                'login_date': row[u'Senaste inloggning'] or False,
                                'groups_id': [(6, 0, [portal.id])],
                            })

                    # Create delivery adress data.
                    for values in delivery_users:
                        partner = values['partner_id']
                        if values['exid'] in users:
                            # User exists. Add the delivery adress to user partner.
                            partner.drupal_parent_ids |= users[values['exid']].partner_id
                        else:
                            # Create a new user with delivery adress as partner.
                            exid = values['exid']
                            del values['exid']
                            values['partner_id'] = partner.id
                            users[exid] = importf.env['res.users'].with_context({'no_reset_password': True}).create(
                                values)
                            importf.set_external_id(users[exid], exid)

                    # Create users without customer data.
                    for values in unknown_users:
                        if values['exid'] not in users:
                            exid = values['exid']
                            del values['exid']
                            users[exid] = importf.env['res.users'].with_context({'no_reset_password': True}).create(
                                values)
                            importf.set_external_id(users[exid], exid)

            except Exception as e:
                try:
                    # Close the ssh session, if it exists
                    importf.session.close()
                    importf.transport.close()
                except:
                    pass
                # Reraise after terminating ssh connection
                raise e
            try:
                # Close the ssh session, if it exists
                importf.session.close()
                importf.transport.close()
            except:
                pass
            importf.password = ''

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
        if not name:
            return False
        country = self.env['res.country'].search([('name', '=', name)])
        if not country and len(country) == 1:
            raise Warning("Couldn't find a match for country %s" % name)
        return country.id

    @api.model
    def find_state(self, name, country_id):
        if not name:
            return False
        state = self.env['res.country.state'].search([('name', '=', name), ('country_id', '=', country_id)])
        if not state:
            state = self.env['res.country.state'].create({'name': name, 'country_id': country_id, 'code': 'ABC'})
        return state.id

    @api.model
    def download_image(self, image_name, dir='/var/lib/drupal7/files/cavarosawine_se/'):
        # TODO: Use Paramiko SFTP instead
        if not (hasattr(self, 'session') and self.session):
            import paramiko
            self.transport = paramiko.Transport(('wiggum.vertel.se', 22))
            self.transport.connect(username=self.username, password=self.password)
            self.session = paramiko.SFTPClient.from_transport(self.transport)
        image = ''
        if image_name:
            try:
                with self.session.open(dir + image_name.split(' (')[0].strip(), 'r') as f:
                    image = base64.b64encode(f.read())
            except:
                _logger.warn("Couldn't get %s" % dir + image_name.split(' (')[0].strip())
        return image
