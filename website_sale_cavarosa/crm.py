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
from openerp.addons.website_sale.controllers.main import website_sale
import logging
_logger = logging.getLogger(__name__)

class crm_tracking_campaign(models.Model):
    _inherit = 'crm.tracking.campaign'
    _mail_mass_mailing = _('Campaign')


class website(models.Model):
    _inherit = 'website'

    def current_campaign(self):
        return self.env['crm.tracking.campaign'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today())])


class website_sale(website_sale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(force_create=1)
        order._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        if kw.get('campaign_id'):
            order.write({'campaign_id': kw.get('campaign_id')})
        return request.redirect("/shop/cart")


class current_campaign(http.Controller):

    @http.route(['/shop/campaign'], type='http', auth="user", website=True)
    def campaign(self, **post):
        campaigns = request.website.current_campaign()
        if len(campaigns) > 0:
            return request.website.render('website_sale_cavarosa.current_campaign', {'campaign': campaigns[0]})
        else:
            campaigns = request.env['crm.tracking.campaign'].search([('date_start', '>=', fields.Date.today())])
            if len(campaigns) > 0:
                next_campaign_date = campaigns[0].date_start
                for c in campaigns:
                    if c.date_start < next_campaign_date:
                        next_campaign_date = c.date_start
                return request.website.render('website_sale_cavarosa.no_campaign', {'next_campaign_date': next_campaign_date})
            else:
                return request.website.render('website_sale_cavarosa.no_campaign', {'next_campaign_date': None})
