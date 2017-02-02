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
from openerp import http
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class crm_tracking_campaign(models.Model):
    _inherit = 'crm.tracking.campaign'
    _mail_mass_mailing = _('Campaign')

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    partner_ids = fields.Many2many(string='Suppliers', comodel_name='res.partner')
    product_ids = fields.Many2many(string='Products', comodel_name='product.template')
    description = fields.Html(string='Description', sanitize=False)

class current_campaign(http.Controller):

    @http.route(['/shop/campaign'], type='http', auth="user", website=True)
    def campaign(self, **post):
        campaigns = request.env['crm.tracking.campaign'].search([('date_start', '<=', fields.Date.today()), ('date_end', '>=', fields.Date.today())])
        if len(campaigns) > 0:
            return request.website.render('website_sale_cavarosa.current_campaign', {'campaigns': campaigns})
        else:
            return request.website.render('website_sale_cavarosa.current_campaign', {})
