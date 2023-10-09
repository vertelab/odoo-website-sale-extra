from datetime import datetime, date
from odoo import http
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(force_create=1)
        order._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        if kw.get('campaign_id'):
            order.write({'campaign_id': kw.get('campaign_id')})
        return request.redirect("/shop/cart")


class CurrentCampaign(http.Controller):
    @http.route(['/campaign', '/campaign/<model(""):campaigns>'], type='http', auth="public", website=True)
    def campaign(self, campaigns=None, **post):
        if not campaigns:
            campaigns = request.website.sudo().current_campaign()
        if len(campaigns) > 0:
            print(campaigns)
            return request.render('website_sale_cavarosa.current_campaign', {'campaign': campaigns[0]})
        else:
            campaigns = request.env['utm.campaign'].sudo().search([('date_start', '>=', date.today())])
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
                s = {'supplier_url': '/producer/%s' % o.object_id.id, 'supplier_name': o.object_id.name,
                     'supplier_image': '/website/imagemagick/res.partner/image/%s/%s' % (
                         o.object_id.id, request.env.ref('website_sale_cavarosa.img_supplier_nav').id)}
                supplier_list.append(s)
        return supplier_list
