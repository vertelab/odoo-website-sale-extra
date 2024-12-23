# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    def current_campaign(self):
        res = self.env['utm.campaign'].sudo().search([
            ('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today())
        ],limit=1)
        return res

    def _prepare_sale_order_values(self, partner_sudo):
        self.ensure_one()
        values = super(Website, self)._prepare_sale_order_values(partner_sudo)
        values['campaign_id'] = request.website.current_campaign().id if request.website.current_campaign() else None
        return values
