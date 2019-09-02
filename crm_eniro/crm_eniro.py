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

from odoo import models, fields, api, _
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from odoo.exceptions import Warning
import urllib.parse
import logging
import re
import requests

_logger = logging.getLogger(__name__)

class crm_lead(models.Model):
    _inherit = "crm.lead"
    # start: res_partner.py from l10n_se
    company_registry = fields.Char(string='Company Registry', size=11)

    @api.one
    def get_company_info_registry(self):

        if self.company_registry and (len(self.company_registry) > 0):

            api_profile = self.env['ir.config_parameter'].sudo().get_param('eniro_api.profile')
            api_key = self.env['ir.config_parameter'].sudo().get_param('eniro_api.key')
            if not (api_key or api_profile):
                raise Warning('Please configurate Eniro api account, %s , %s' % (api_profile, api_key) )

            try:
                res = requests.get(u'http://api.eniro.com/partnerapi/cs/search/basic?profile=%s&key=%s&country=se&version=1.1.3&search_word=%s' % (api_profile, api_key, self.company_registry ))
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
            _logger.info('<<<<<< API Eniro Result: %s >>>>>' % res)
            
           # (true,false,null) = (True,False,None) ## eval needs this!
            json = res.json()
            _logger.info('<<<<<< API Eniro Result: %s >>>>>' % json)

            if not json or len(json['adverts']) == 0 or json['totalHits'] == 0:
                return False

            adverts = json['adverts'][0]
            _logger.debug('<<<<<< Adverts: %s >>>>>' % adverts)
            companyInfo = adverts['companyInfo']
            address = adverts['address']
            phoneNumbers = adverts['phoneNumbers']
            location = adverts['location']

            if not adverts['homepage'] == None:
                homepage = adverts['homepage']
                homepage = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urlopen(homepage).read().decode('utf-8'))[1]
            else:
                homepage = None

            self.write({
                'name': companyInfo['companyName'],
                'partner_name': companyInfo['companyName'],
                'street': address['streetName'],
                'street2': address['postBox'] or '',
                'zip': address['postCode'],
                'city': address['postArea'],
                'phone': [pn['phoneNumber'] for pn in phoneNumbers if pn['type'] == 'std'][0] if len(phoneNumbers)>0 else '',
                # ~ 'partner_latitude': location['coordinates'][0]['latitude'],
                # ~ 'partner_longitude': location['coordinates'][0]['longitude'],
                'website': homepage,
                'country_id': self.env['res.country'].search([('code','=','SE')])[0].id,
            })

        return json

    @api.one
    def get_company_info(self):

        if self.name and (len(self.name) > 0):

            api_profile = self.env['ir.config_parameter'].sudo().get_param('eniro_api.profile')
            api_key = self.env['ir.config_parameter'].sudo().get_param('eniro_api.key')
            if not (api_key or api_profile):
                raise Warning('Please configurate Eniro api account, %s , %s' % (api_profile, api_key) )

            try:
                res = requests.get(u'http://api.eniro.com/partnerapi/cs/search/basic?profile=%s&key=%s&country=se&version=1.1.3&search_word=%s' % (api_profile, api_key, self.name ))
                # ~ raise Warning(res.json().keys() )
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
            _logger.info('<<<<<< API Eniro Result: %s >>>>>' % res)
            
           # (true,false,null) = (True,False,None) ## eval needs this!
            json = res.json()
            _logger.info('<<<<<< API Eniro Result: %s >>>>>' % json)

            if not json or len(json['adverts']) == 0 or json['totalHits'] == 0:
                return False

            adverts = json['adverts'][0]
            _logger.debug('<<<<<< Adverts: %s >>>>>' % adverts)
            companyInfo = adverts['companyInfo']
            address = adverts['address']
            phoneNumbers = adverts['phoneNumbers']
            location = adverts['location']

            if not adverts['homepage'] == None:
                homepage = adverts['homepage']
                homepage = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urlopen(homepage).read().decode('utf-8'))[1]
            else:
                homepage = None

            self.write({
                'name': companyInfo['companyName'],
                'partner_name': companyInfo['companyName'],
                'street': address['streetName'],
                'street2': address['postBox'] or '',
                'zip': address['postCode'],
                'city': address['postArea'],
                'phone': [pn['phoneNumber'] for pn in phoneNumbers if pn['type'] == 'std'][0] if len(phoneNumbers)>0 else '',
                # ~ 'partner_latitude': location['coordinates'][0]['latitude'],
                # ~ 'partner_longitude': location['coordinates'][0]['longitude'],
                'company_registry': '%s-%s' % (companyInfo['orgNumber'][0:6], companyInfo['orgNumber'][-4:]),
                'website': homepage,
                'country_id': self.env['res.country'].search([('code','=','SE')])[0].id,
            })

        return json

    @api.multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """ extract data from lead to create a partner
            :param name : furtur name of the partner
            :param is_company : True if the partner is a company
            :param parent_id : id of the parent partner (False if no parent)
            :returns res.partner record
        """
        res = super(crm_lead, self)._create_lead_partner_data(name, is_company, parent_id)
        res.update({ 'company_registry': self.company_registry })
        return res
        
        
