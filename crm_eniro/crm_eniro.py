# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
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
import urllib2
import logging
import re
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_company_info(self):

        if self.is_company and self.vat and (len(self.vat) > 0):

            api_profile = self.env['ir.config_parameter'].sudo().get_param('eniro_api_profile')
            api_key = self.env['ir.config_parameter'].sudo().get_param('eniro_api_key')
            if not (api_key or api_profile):
                raise Warning('Please configurate Eniro api account')

            try:
                res = urllib2.urlopen('http://api.eniro.com/partnerapi/cs/search/basic?profile=%s&key=%s&country=se&version=1.1.3&search_word=%s' % (api_profile, api_key, self.company_registry)).read()
                (true,false,null) = (True,False,None) 
            except urllib2.HTTPError as e:
                _logger.error('api.eniro error: %s %s' % (e.code, e.reason))
                if e.code == 401:
                    _logger.error('Eniro API %s %s (wrong profile/key)' % (e.code, e.reason))
                    raise Warning('Eniro API %s %s (wrong profile/key)' % (e.code, e.reason))
                return False
            except urllib2.URLError as e:
                _logger.error('api.eniro url error: %s %s' % (e.code, e.reason))
                return False
            
            json = eval(res)
            _logger.info('<<<<<< API Eniro Result: %s >>>>>' % json)

            if not json or len(json['adverts']) == 0 or json['totalHits'] == 0:
                return False

            adverts = json['adverts'][json['totalHits']-1]
            _logger.debug('<<<<<< Adverts: %s >>>>>' % adverts)
            companyInfo = adverts['companyInfo']
            address = adverts['address']
            phoneNumbers = adverts['phoneNumbers']
            location = adverts['location']
            if not adverts['homepage'] == None:
                homepage = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urllib2.urlopen(adverts['homepage']).read())[1]
            else:
                homepage = None

            self.write({
                'name': companyInfo['companyName'],
                'street': address['streetName'],
                'street2': address['postBox'] or '',
                'zip': address['postCode'],
                'city': address['postArea'],
                'phone': [pn['phoneNumber'] for pn in phoneNumbers if pn['type'] == 'std'][0] if len(phoneNumbers)>0 else '',
                'partner_latitude': location['coordinates'][0]['latitude'],
                'partner_longitude': location['coordinates'][0]['longitude'],
                'website': homepage,
                'country_id': self.env['res.country'].search([('code','=','SE')])[0].id,
            })

        return json
