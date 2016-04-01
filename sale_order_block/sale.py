# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import openerp
import werkzeug
import pytz
import re

import logging
_logger = logging.getLogger(__name__)

class sale_order_skill(models.Model):
    _name = 'sale.order.skill'
    categ_id = fields.Many2one(comodel_name='crm.case.categ')
    order_id = fields.Many2one(comodel_name='sale.order', string='Order')
    level = fields.Selection([('1','< 1 year'),('2', '1 - 3 years'),('3', '3 - 5 years'),('4', '> 5 years')],string='Level', required=False)


class sale_order(models.Model):
    _inherit = ['sale.order']#,'mail.thread']
    
    website_published = fields.Boolean()
    #~ @api.one
    #~ def _website_short_description(self):
        #~ self.website_short_description = re.match(re.compile('(^.*\.)'),self.website_description[:25]) and re.match(re.compile('(^.*\.)'),self.website_description[:25]).group() or self.website_description[:25]
    #~ website_short_description = fields.Text(compute="_website_short_description")
    website_description = fields.Text(string="Description",size=100,help="Use this box for describing the quotation.")
    website_subject = fields.Char(size=25)
    skill_ids = fields.One2many(comodel_name='sale.order.skill',inverse_name='order_id', string='Skills')
    
    language_ids = fields.Many2many(comodel_name='hr.language', string='Languages')
    location_ids = fields.Many2many(comodel_name='hr.location', string='Places')
    
    date_start = fields.Date(string = "Start Date")
    date_stop = fields.Date(string = "Stop Date")
    #~ uom_categ_wtime = self.env.ref("product.uom_categ_wtime")
    @api.one
    def _categ_wtime_id(self):
        self.categ_wtime_id = self.env.ref("product.uom_categ_wtime").id
    categ_wtime_id = fields.Integer(compute='_categ_wtime_id')
    uom_id = fields.Many2one(comodel_name='product.uom',string='Unit of measure' )
    qty = fields.Float(string="Quantity")
            

class website_product_category(http.Controller):
    @http.route(['/so/<model("sale.order"):order>/interest'], type='json', auth="user")
    def sale_order_interest(self, order = None, **post):
        if order:
            partner = request.env['res.users'].browse(request.context.get("uid")).partner_id
            request.env['mail.message'].create({
                'body': _("Yes, I'm interested in %s" % order.name),
                'subject': 'Interested',
                'author_id': partner.id,
                'res_id': order.id,
                'model': order._name,
                'type': 'notification',})                
        #~ return http.local_redirect('/')
        return _('Thanks for shown interest.')
        
    @http.route(['/sale_order_block',], type='http', auth="public", website=True)
    def index(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('sale_order_block.index', {
        })
    
    @http.route(['/senaste_uppdragen',], type='http', auth="public", website=True)
    def senaste_uppdragen(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('sale_order_block.senaste_uppdragen', {
        })
    
    @http.route(['/jobba_hos_oss',], type='http', auth="public", website=True)
    def work_with_us(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('sale_order_block.work_with_us', {
        })
        
    @http.route(['/hitta_konsult',], type='http', auth="public", website=True)
    def hitta_konsult(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return request.render('sale_order_block.hitta_konsult', {
        })
        
    
class contactus(openerp.addons.website_crm.controllers.main.contactus):
    def create_lead(self, request, values, kwargs):
        #~ action_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, request.uid, path_or_xml_id_or_id, raise_if_not_found=False)
        
        path_or_xml_id_or_id = "website_crm." + values['categ_ids']
        #~ path_or_xml_id_or_id = "website_crm.consultant"
        
        #~ raise Warning(path_or_xml_id_or_id)
        
        action_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, request.uid, path_or_xml_id_or_id, raise_if_not_found=False)
        #~ modul prefix sale_order_block.consultant -> path_or_xml_id_or_id
        
        #~ Add hidden specific TAG to Lead, depending on form.
        values['categ_ids'] = [(6,0,[action_id])]
        return super(contactus,self).create_lead(request, values, kwargs)














