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
import urllib2
import logging
import re
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    def copy_company_info(self):

        if self.is_company and (len(self.vat) > 0):
            api_profile = self.env['ir.config_parameter'].sudo().get_param('eniro_api_profile')
            api_key = self.env['ir.config_parameter'].sudo().get_param('eniro_api_key')
            if not (api_key or api_profile):
                raise Warning('Please configurate Eniro api account')
            res = urllib2.urlopen('http://api.eniro.com/partnerapi/cs/search/basic?profile=%s&key=%s&country=se&version=1.1.3&search_word=%s' % (api_profile, api_key, self.company_registry)).read()
            (true,false,null) = (True,False,None)
            json = eval(res)
            if not json and json['totalHits'] == 0:
                pass

            else:
                for advert in json['adverts']:
                    #~ print advert['companyInfo']['companyName']
                    pass

                companyInfo = json['adverts'][0]['companyInfo']
                address = json['adverts'][0]['address']
                phoneNumbers = json['adverts'][0]['phoneNumbers']
                location = json['adverts'][0]['location']
                homepage = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urllib2.urlopen(json['adverts'][0]['homepage']).read())[1]

                self.write({
                    'name': companyInfo['companyName'],
                    'street': address['streetName'],
                    # 'street2': address['postBox'],
                    'zip': address['postCode'],
                    'city': address['postArea'],
                    'phone': [pn['phoneNumber'] for pn in phoneNumbers if pn['type'] == 'std'][0],
                    'latitude': location['coordinates'][0]['latitude'],
                    'longitude': location['coordinates'][0]['longitude'],
                    'website': homepage,
                })

        return True
