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
import base64
from cStringIO import StringIO

from subprocess import Popen, PIPE
import os
import tempfile
try:
    from xlrd import open_workbook, XLRDError
    from xlrd.book import Book
    from xlrd.sheet import Sheet
except:
    _logger.info('xlrd not installed.')

import logging
_logger = logging.getLogger(__name__)

try:
    import unicodecsv as csv
except:
    _logger.info('Missing unicodecsv. sudo pip install unicodecsv')


class DermanordImport(models.TransientModel):
    _name = 'sale.dermanord.import.wizard'

    order_file = fields.Binary(string='Order file')
    mime = fields.Selection([('pdf','application/pdf'),('excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')])
    import_type = fields.Selection([('lyko','Lyko Online AB'),('finamig','Fina mig i Hedemora AB'),('skincity','SKINCITY SWEDEN AB')])
    info = fields.Text(string='Info')
    tmp_file = fields.Char(string='Tmp File')
    
    @api.one
    @api.onchange('order_file')
    def check_file(self):
        self.mime = None
        self.import_type = None
        self.info = None
        self.tmp_file = None
        
        if self.order_file:
            fd, self.tmp_file = tempfile.mkstemp()
            os.write(fd, base64.b64decode(self.order_file))
            os.close(fd)

            try:
                pop = Popen(['file','-b','--mime',self.tmp_file], shell=False, stdout=PIPE)
                (result, _) = pop.communicate()
                read_mime = result.split(';')[0]
            except OSError,e:
                _logger.warning("Failed attempt to execute file. This program is necessary to check MIME type of %s", fname)
                _logger.debug("Trace of the failed MIME file attempt.", exc_info=True)
                raise Warning(e)


            self.mime = self.get_selection_text('mime',read_mime)
            if self.mime == 'pdf':
                try:
                    pop = Popen(['pdftotext', '-enc', 'UTF-8', '-nopgbrk', self.tmp_file, '-'], shell=False, stdout=PIPE)
                    (content, _) = pop.communicate()
                except OSError,e:
                    _logger.warning("Failed attempt to execute pdftotext. This program is necessary to index the file %s of MIME type %s. Detailed error available at DEBUG level.", self.tmp_file, self.mime)
                    _logger.debug("Trace of the failed file indexing attempt.", exc_info=True)
                    raise Warning(e)
                lines = content.splitlines()
                if len(lines)>=19 and lines[19] == 'Fina mig i Hedemora AB':
                    self.import_type = 'finamig'
                elif 'SKINCITY SWEDEN AB' in content:
                    self.import_type = 'skincity'
            elif self.mime == 'excel':
                try:
                    wb = open_workbook(file_contents=base64.b64decode(self.order_file)).sheet_by_index(0)
                except XLRDError, e:
                    raise Warning(e)

                if wb.cell_value(0,2) == u'Lyko Artikelnr':
                    self.import_type = 'lyko'
            self.info = '%s\n%s' % (self.get_selection_value('import_type',self.import_type),self.get_selection_value('mime',self.mime))


        
    @api.one
    def import_files(self):
        order = None
        if self[0].mime == 'pdf':
            try:
                #~ pop = Popen(['pdftotext', '-enc', 'UTF-8', '-nopgbrk', fname, '-'], shell=False, stdout=PIPE)
                pop = Popen(['pdf2txt.py', self.tmp_file], shell=False, stdout=PIPE)
                (content, _) = pop.communicate()
            except OSError,e:
                _logger.warning("Failed attempt to execute pdf2txt.py. This program is necessary to decode the file %s of MIME type %s. Detailed error available at DEBUG level.", self.tmp_file, self.mime)
                _logger.debug("Trace of the failed file indexing attempt.", exc_info=True)
                raise Warning(e)
            lines = content.splitlines()
#
#   Fina mig i Hedemora AB
#
            if self[0].import_type == 'finamig':
                customer = self.env['res.partner'].search([('name','=',self.get_selection_value('import_type',self.import_type))])
                artnr =  []
                antal = []
                for line in range(0,len(lines)):
                    _logger.warn('Line %s|' % lines[line])
                    if lines[line] == 'Art. Nr':
                        line += 1
                        for art in range(line,len(lines)):
                            if lines[art] == '':
                                line = art
                                break
                            _logger.warn('Art Nr %s' % lines[art])
                            artnr.append(lines[art].replace('(cid:160)',''))
                    if lines[line] == 'Antal':
                        for ant in range(line+1,len(artnr)+line):
                            _logger.warn('Antal %s' % lines[ant])
                            antal.append(int(lines[ant].replace(' st','')))
                        line += len(antal)
                    if lines[line] == 'Ordernummer':
                        line += 1
                        ordernummer = lines[line]
                    if lines[line] == 'Orderdatum':
                        line += 1
                        orderdatum = lines[line]
                    line += 1
                order = self.env['sale.order'].create({
                    'partner_id': customer.id,
                    'client_order_ref': ordernummer,
                    'date_order': orderdatum,
                })
                for i,art in enumerate(artnr):
                    _logger.warn('products: %s %s' % (i,art))
                    product = self.env['product.product'].search([('default_code','=',art)])
                    if product:
                        self.env['sale.order.line'].create({
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': antal[i],
                        })
                                
#
#    Skincity   
#
            elif self[0].import_type == 'skincity':
                customer = self.env['res.partner'].search([('name','=',self.get_selection_value('import_type',self.import_type))])
                artnr =  []
                antal = []
                for line in range(0,len(lines)):
                    _logger.warn('Line %s|' % lines[line])
                    if lines[line] == 'Beskrivning':
                        line += 1
                        for art in range(line,len(lines)):
                            if lines[art] == '':
                                line = art
                                break
                            _logger.warn('Art Nr %s' % lines[art].split()[0])
                            artnr.append(lines[art].split()[0])
                    if lines[line] == 'Antal':
                        for ant in range(line+1,len(artnr)+line):
                            _logger.warn('Antal %s' % lines[ant])
                            antal.append(int(lines[ant]))
                        line += len(antal)
                    if lines[line] == 'Inköpsorder':
                        ordernummer = lines[line].split()[1]
                    if lines[line] == 'Orderdatum':
                        line += 5
                        orderdatum = lines[line]
                    line += 1
                order = self.env['sale.order'].create({
                    'partner_id': customer.id,
                    'client_order_ref': ordernummer,
                    'date_order': orderdatum,
                })
                for i,art in enumerate(artnr):
                    _logger.warn('products: %s %s' % (i,art))
                    product = self.env['product.product'].search([('default_code','=',art)])
                    if product:
                        self.env['sale.order.line'].create({
                            'order_id': order.id,
                            'product_id': product.id,
                            'product_uom_qty': antal[i],
                        })




                
        elif self[0].mime == 'excel':
            try:
                wb = open_workbook(file_contents=base64.b64decode(self.order_file)).sheet_by_index(0)
            except XLRDError, e:
                raise ValueError(e)

#
# Lyko
#
            if self[0].import_type == 'lyko':
                customer = self.env['res.partner'].search([('name','=',self.get_selection_value('import_type',self.import_type))])
                order = self.env['sale.order'].create({
                    'partner_id': customer.id,
                    'client_order_ref': wb.cell_value(1,0),
                })
                l = 1
                for line in range(l,wb.nrows):
                    if wb.cell_value(line,4) not in [u'Ert artikelnr','']:
                        product = self.env['product.product'].search([('default_code','=',wb.cell_value(line,4))])
                        if product:
                            _logger.warn('Rad %s  %s' % (wb.cell_value(line,4),wb.cell_value(line,6)))
                            self.env['sale.order.line'].create({
                                        'order_id': order.id,
                                        'product_id': product.id,
                                        'product_uom_qty': int(wb.cell_value(line,6)),
                                    })
                                    
#
# END
#
        if order:
            attachment = self.env['ir.attachment'].create({
                    'name': order.client_order_ref,
                    'res_name': order.name,
                    'res_model': 'sale.order',
                    'res_id': order.id,
                    'datas': base64.encodestring(self.import_file),
                    'datas_fname': order.client_order_ref,
                })
            #~ if attachment.mimetype == 'application/pdf':
                #~ attachment.pdf2image(800,1200)

        return {'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_type': 'form',
                'view_mode': 'form',
                 'view_id': self.env.ref('sale.view_order_form').id,
                 'res_id': order.id if order else None,
                 'target': 'new',
                 'context': {},
                 }


                                    
    def get_selection_text(self,field,value):
        for type,text in self.fields_get([field])[field]['selection']:
                if text == value:
                    return type
        return None

    def get_selection_value(self,field,value):
        for type,text in self.fields_get([field])[field]['selection']:
                if type == value:
                    return text
        return None
