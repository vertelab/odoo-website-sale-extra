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
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class loyalty_program(models.Model):
    _name = 'loyalty.program'
    
    name = fields.Char('Name', select=True, required=True)
    #rounding = fields.Float('Points Rounding')
    rule_ids = fields.One2many('loyalty.rule','loyalty_program_id','Rules')
    reward_ids = fields.One2many('loyalty.reward','loyalty_program_id','Rewards')
    
    @api.model
    def calculate_loyalty_points(self, product, qty, price):
        for rule in self.rule_ids.sorted(lambda r: r.sequence):
            if rule.check_match(product, qty, price):
                return rule.calculate_points(product, qty, price)
        return 0
    

class loyalty_rule(models.Model):
    _name = 'loyalty.rule'
    
    name = fields.Char('Name', select=True, required=True)
    loyalty_program_id = fields.Many2one('loyalty.program', 'Loyalty Program')
    product_id = fields.Many2one('product.product','Target Product')
    category_id = fields.Many2one('product.category', 'Target Category')
    sequence = fields.Float('Sequence', default=100)
    product_points = fields.Float('Points per product')
    currency_points = fields.Float('Points per currency')
    
    @api.multi
    def check_match(self, product, qty, price):
        self.ensure_one()
        def is_child_of(p_categ, c_categ):
            if p_categ == c_categ:
                return True
            elif not c_categ.parent_id:
                return False
            else:
                return is_child_of(p_categ, c_categ.parent_id)
        #Add quantity to rules matching?
        return (not self.product_id or self.product_id == product) and (not self.category_id or is_child_of(self.category_id, product.categ_id))
    
    @api.multi
    def calculate_points(self, product, qty, price):
        self.ensure_one()
        return self.product_points * qty + self.currency_points * price

class loyalty_reward(models.Model):
    _name = 'loyalty.reward'
    
    name = fields.Char('Name', select=True, required=True)
    loyalty_program_id = fields.Many2one('loyalty.program', 'Loyalty Program', help='The Loyalty Program this reward belongs to')
    type = fields.Selection([('gift','Gift'),('discount','Discount'),('resale','Resale')], 'Type', required=True)
    gift_product_id = fields.Many2one('product.product','Gift Product', help='The product given as a reward')
    point_cost = fields.Float('Point Cost', help='The cost of the reward')
    discount = fields.Float('Discount',help='The discount percentage')

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    loyalty_points = fields.Float('Loyalty Points')

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    loyalty_program_id = fields.Many2one('loyalty.program', 'Loyalty Program')
    loyalty_points = fields.Float('Loyalty Points', compute='get_loyalty_points', store=True)
    
    @api.one
    @api.depends('product_id', 'product_uom_qty', 'price_subtotal', 'order_id.loyalty_program_id')
    def get_loyalty_points(self):
        if self.order_id.loyalty_program_id:
            self.loyalty_points = self.order_id.loyalty_program_id.calculate_loyalty_points(self.product_id, self.product_uom_qty, self.price_subtotal)

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    loyalty_program_id = fields.Many2one('loyalty.program', 'Loyalty Program')
    loyalty_points = fields.Float('Loyalty Points', compute='get_loyalty_points', store=True)
    
    @api.depends('order_line', 'order_line.product_id', 'order_line.product_uom_qty', 'order_line.price_subtotal')
    def get_loyalty_points(self):
        points = 0
        for line in self.order_line:
            points += line.loyalty_points
        self.loyalty_points = points
    
    @api.multi
    def action_button_confirm(self):
        res = super(sale_order, self).action_button_confirm()
        if res:
            for order in self:
                order.partner_id.loyalty_points += order.loyalty_points
        return res
            
             
    
