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
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import werkzeug
import pytz
import re
import base64
from fnmatch import fnmatch,fnmatchcase
from lxml import etree
import openerp.tools as tools
import openerp.tools.misc as misc
from tempfile import TemporaryFile


import logging
_logger = logging.getLogger(__name__)

class product_upload(models.TransientModel):
    _name = 'product.upload'
    _description = 'Upload products from CSV-file'
    _order = 'name'

    data = fields.Binary('File')
    @api.one
    def _data(self):
        self.xml_file = self.data
    xml_file = fields.Binary(compute='_data')
    def _periods(self):
        return [p.id for p in self.env['account.period'].search([])]
    period_ids = fields.Many2many('account.period',default=_periods)
    description = fields.Text('Note', help="This will be included in the message")
    state =  fields.Selection([('choose', 'choose'), ('get', 'get')],default="choose") 
    depth =  fields.Selection([('0', 'none'), ('1', '1 level'), ('2', '2 levels'), ('3', '3 levels'), ('4', '4 levels')],default="0") 
    name = fields.Char('File Name', readonly=True)
    #model = fields.Selection([('res.partner','Customers'),('account.invoice','Invoices'),('account.move','Moves')],string="Model")
    model = fields.Many2one(comodel_name='ir.model',string="Model")
    model_ids = fields.Many2many(comodel_name="ir.model")

    has_period = fields.Boolean('Has Period')


   
    @api.multi
    def send_form(self,):
        import csv
        product = self[0]
        #_logger.warning('data %s b64 %s ' % (account.data,base64.decodestring(account.data)))
        if not product.data == None:
            fileobj = TemporaryFile('w+')
            fileobj.write(base64.decodestring(product.data))
            fileobj.seek(0)
 
            try:
                for row in csv.DictReader(fileobj):
                    pass                
            finally:
                fileobj.close()
            return True
        #product.write({'state': 'get', 'name': '%s.xml' % account.model.model.replace('.','_'),'data': base64.b64encode(account._export_xml()) })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': product.id,
            'views': [(False, 'form')],
            'target': 'new',
        }


