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

class kodspecialisterna_sale_order(models.Model):
    _inherit = 'sale.order'
    website_published = fields.Boolean()
    
class Kodspecialisterna(http.Controller):
    @http.route('/kodspecialisterna', auth='public')
    def index(self, **kw):
        Active_orders = http.request.env['sale.order']
        return request.render('kodspecialisterna.index', {
            'active_orders': Active_orders.search([('state','=','draft')])
        })

class website_product_category(http.Controller):

    @http.route(['/category/<model("product.category"):category>', ], type='http', auth="public", website=True)
    def get_products(self, category=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('kodspecialisterna.page_behandling', {'products': request.env['product.template'].sudo().search(['&', ('categ_id', '=', category.id), ('state', '=', 'sellable')], order='website_sequence'), 'category': category})
        if category and not category.website_published:
            return request.render('website.page_404', {})
        else:
            pass
            
    @http.route(['/order/<model("sale.order"):order>', ], type='http', auth="public", website=True)
    def get_order(self, order=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('sale_order_block.page_order', {'order':order})
        
    
    @http.route(['/allcategory/<model("product.category"):category>', ], type='http', auth="public", website=True)
    def get_category(self, parent_id=1, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        categories = request.env['product.category'].sudo().search([('parent_id', '=', parent_id)], order='id')
        #categories.filtered("category.is_translated(lang)")
        return request.render('website_product_category.page_allcategories', {'categories': categories})
        
class product_category(models.Model):
    _inherit = "product.category"
    
    website_description = fields.Html('Description for the website', translate=True, sanitize=False)
    website_small_description = fields.Html('Short description', translate=True, sanitize=False)
    website_published = fields.Boolean('Available in the website', copy=False)
    website_image = fields.Binary('Category Image')

    def is_translated(self,lang):
        return len(self.env['ir.translation'].search(['&',('name','=','product.category,website_small_description'),('lang','=',lang)])) == 1

