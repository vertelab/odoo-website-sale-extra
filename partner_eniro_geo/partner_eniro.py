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

from odoo import models, fields, api, _
import logging
import re
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    def get_company_info(self):
        res = super().get_company_info()
        if res:
            adverts = res['adverts'][res['totalHits']-1]
            location = adverts['location']
            self.write({
                'partner_latitude': location['coordinates'][0]['latitude'] if len(location['coordinates']) else '',
                'partner_longitude': location['coordinates'][0]['longitude'] if len(location['coordinates']) else '',
            })
        return res
