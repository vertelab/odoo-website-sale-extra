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
from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class crm_tracking_campaign(models.Model):
    _inherit = 'utm.campaign'
    _mail_mass_mailing = _('Campaign')

    estimated_delivery = fields.Date(string='Estimated delivery')


class website(models.Model):
    _inherit = 'website'

    def current_campaign(self):
        return self.env['utm.campaign'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today())])


class website_sale(http.Controller):
    _inherit = 'WebsiteSale'

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(force_create=1)
        order._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        if kw.get('campaign_id'):
            order.write({'campaign_id': kw.get('campaign_id')})
        return request.redirect("/shop/cart")


class current_campaign(http.Controller):

    @http.route(['/campaign', '/campaign/<model(""):campaigns>'], type='http', auth="public", website=True)
    def campaign(self, campaigns=None, **post):
        if not campaigns:
            campaigns = request.website.sudo().current_campaign()
        if len(campaigns) > 0:
            return request.render('website_sale_cavarosa.current_campaign', {'campaign': campaigns[0]})
        else:
            campaigns = request.env['utm.campaign'].sudo().search([('date_start', '>=', fields.Date.today())])
            if len(campaigns) > 0:
                next_campaign_date = campaigns[0].date_start
                for c in campaigns:
                    if c.date_start < next_campaign_date:
                        next_campaign_date = c.date_start
                return request.render('website_sale_cavarosa.no_campaign', {'next_campaign_date': next_campaign_date})
            else:
                return request.render('website_sale_cavarosa.no_campaign', {'next_campaign_date': None})

    @http.route(['/snippet/get_campaign'], type='json', auth="user", website=True)
    def get_campaign(self, campaign_id=None, **kw):
        campaign = request.env['utm.campaign'].browse(int(campaign_id))
        supplier_list = []
        for o in campaign.object_ids:
            if o.object_id._name == 'res.partner':
                s = {}
                s['supplier_url'] = '/producer/%s' %o.object_id.id
                s['supplier_name'] = o.object_id.name
                s['supplier_image'] = '/website/imagemagick/res.partner/image/%s/%s' %(o.object_id.id, request.env.ref('website_sale_cavarosa.img_supplier_nav').id)
                supplier_list.append(s)
        return supplier_list
