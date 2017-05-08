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
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    name = fields.Text(states={'draft': [('readonly', False)], 
                               'confirmed': [('readonly', False)],
                               'exception': [('readonly', False)],
                                         })
class sale_order(models.Model):
    _inherit = 'sale.order'
    
    #'order_line': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True),
    order_line = fields.One2many(states={'draft': [('readonly', False)], 
                                         'sent': [('readonly', False)],
                                         'waiting_date': [('readonly', False)],
                                         'progress': [('readonly', False)],
                                         'manual': [('readonly', False)],                                         
                                         })
