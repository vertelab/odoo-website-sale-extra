# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
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

from odoo import models, fields, api, _
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import logging
import re
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    # start: res_partner.py from l10n_se
    company_registry = fields.Char(compute="_company_registry",inverse='_set_company_registry',string='Company Registry', size=11,readonly=False)
    
    @api.depends('vat')
    def _company_registry(self):
        for partner in self:
            if partner.vat and re.match('SE[0-9]{10}01', partner.vat):
                partner.company_registry = "%s-%s" % (partner.vat[2:8],partner.vat[8:-2])
    
    @api.depends('company_registry')
    def _set_company_registry(self):
        for partner in self:
            if not partner.company_registry: continue
            if not partner.company_registry[6] == '-': continue
            partner.vat = 'SE' + partner.company_registry[:6] + partner.company_registry[7:] + '01'
    # end

    @api.one
    def get_company_info(self):

        if self.is_company and self.vat and (len(self.vat) > 0):

            api_profile = self.env['ir.config_parameter'].sudo().get_param('eniro_api.profile')
            api_key = self.env['ir.config_parameter'].sudo().get_param('eniro_api.key')
            if not (api_key or api_profile):
                raise Warning('Please configurate Eniro api account')

            try:
                #For future reference: use urllib2.quote() to translate the search term to url format.
                res = urlopen('http://api.eniro.com/partnerapi/cs/search/basic?profile=%s&key=%s&country=se&version=1.1.3&search_word=%s' % (api_profile, api_key, self.company_registry)).read()
                (true,false,null) = (True,False,None)
            except HTTPError as e:
                _logger.error('api.eniro error: %s %s' % (e.code, e.reason))
                if e.code == 401:
                    _logger.error('Eniro API %s %s (wrong profile/key)' % (e.code, e.reason))
                    raise Warning('Eniro API %s %s (wrong profile/key)' % (e.code, e.reason))
                return False
            except URLError as e:
                _logger.error('api.eniro url error: %s %s' % (e.code, e.reason))
                return False

            json = eval(res)
            _logger.info('<<<<<< API Eniro **** info Result: %s >>>>>' % json)

            if not json or len(json['adverts']) == 0 or json['totalHits'] == 0:
                return False

            adverts = json['adverts'][0]
            _logger.warn('Eniro <<<<<< Adverts: %s >>>>>' % adverts)
            companyInfo = adverts['companyInfo']
            address = adverts['address']
            phoneNumbers = adverts['phoneNumbers']

            _logger.info('<<<<<< API Eniro **** info Result: %s >>>>>' % json)

            location = adverts['location']
            _logger.warn('Eniro Default value: homepage... test!!' )

            if not adverts['homepage'] == None:
                homepage = adverts['homepage']
                homepage = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urlopen(homepage).read().decode('utf-8'))[1]
            else:
                homepage = None

            self.write({
                'name': companyInfo['companyName'],
                'street': address['streetName'],
                'street2': address['postBox'] or '',
                'zip': address['postCode'],
                'city': address['postArea'],
                'phone': [pn['phoneNumber'] for pn in phoneNumbers if pn['type'] == 'std'][0] if len(phoneNumbers)>0 else '',
                # ~ 'partner_latitude': location['coordinates'][0]['latitude'] if len(location['coordinates']) else '',
                # ~ 'partner_longitude': location['coordinates'][0]['longitude'] if len(location['coordinates']) else '',
                'website': homepage,
                'country_id': self.env['res.country'].search([('code','=','SE')])[0].id,
            })

            return json
