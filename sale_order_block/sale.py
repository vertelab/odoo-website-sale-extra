# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import werkzeug
import pytz
import re


class sale_order(models.Model):
    _inherit = 'sale.order'
    
    website_published = fields.Boolean()
    @api.one
    def _website_short_description(self):
        self.website_short_description = re.match(re.compile('(^.*\.)'),self.website_description[:25]) and re.match(re.compile('(^.*\.)'),self.website_description[:25]).group() or self.website_description[:25]
    website_short_description = fields.Text(compute="_website_short_description")
    website_description = fields.Text(string="Description",size=100,help="Use this box for describing the quotation.")
    website_subject = fields.Char(size=25)

class website_product_category(http.Controller):
    
    @http.route(['/sale_order_block',], type='http', auth="public", website=True)
    def index(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        #~ published = request.env['sale.order'].sudo().search([('website_published','=',True)]).sorted(key=lambda r: r.partner_id.name)
        #~ published = published.sorted(key=lambda r: r.partner_id.name)
        return request.render('sale_order_block.index', {
            #~ 'active_orders': published
        })
    
