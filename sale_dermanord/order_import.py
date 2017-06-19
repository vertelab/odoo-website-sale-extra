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
    
    @api.multi
    def import_files(self):
    

        fd, fname = tempfile.mkstemp()
        os.write(fd, base64.b64decode(self[0].order_file))
        os.close(fd)

        try:
            pop = Popen(['file','-b','--mime',fname], shell=False, stdout=PIPE)
            (result, _) = pop.communicate()
            read_mime = result.split(';')[0]
        except OSError:
            _logger.warning("Failed attempt to execute file. This program is necessary to check MIME type of %s", fname)
            _logger.debug("Trace of the failed MIME file attempt.", exc_info=True)
            return False
            
        mime_type = None
        for type,mime in self.fields_get(['mime'])['mime']['selection']:
            if mime == read_mime:
                #self.mime = type
                mime_type = type
        
        content = None
        if mime_type == 'pdf':
            try:
                pop = Popen(['pdftotext', '-enc', 'UTF-8', '-nopgbrk', fname, '-'], shell=False, stdout=PIPE)
                (content, _) = pop.communicate()
            except OSError:
                _logger.warning("Failed attempt to execute pdftotext. This program is necessary to index the file %s of MIME type %s. Detailed error available at DEBUG level.", fname, self._getMimeTypes()[0])
                _logger.debug("Trace of the failed file indexing attempt.", exc_info=True)

#        
#       Check if Fina Mig AB
#
            lines = content.splitlines()
            if lines[19] == 'Fina mig i Hedemora AB':
                customer = self.env['res.partner'].search([('name','=',lines[19])])
                order = self.env['sale.order'].create({
                    'partner_id': customer.id,
                    'client_order_ref': lines[6],
                    'date_order': lines[10],
                })
                # onchange_partner_id
                i = 0
                for l1 in lines:
                    i += 1
                    if l1 == 'summa':
                        for i in range(i,len(lines)):
                            product = self.env['product.product'].search([('default_code','=',line[i])])
                            if product:
                                qty = lines[i+4].split()[0]
                                self.env['sale.order_line'].create({
                                    'order_id': order.id,
                                    'product_id': product.id,
                                    'product_uom_qty': int(qty) if qty.isdigit() else 1,
                                })
                                
#
#    Skincity   
#
            elif 'SKINCITY SWEDEN AB' in content:
                customer = self.env['res.partner'].search([('name','=','SKINCITY SWEDEN AB')])
                
        elif mime_type == 'excel':
            try:
                wb = open_workbook(file_contents=base64.b64decode(self.order_file)).sheet_by_index(0)
            except XLRDError, e:
                raise ValueError(e)

#
# Lyko
#
            if wb.cell_value(0,2) == u'Lyko Artikelnr':
                customer = self.env['res.partner'].search([('name','=','Lyko Online AB')])
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
                            self.env['sale.order_line'].create({
                                        'order_id': order.id,
                                        'product_id': product.id,
                                        'product_uom_qty': int(wb.cell_value(line,6)),
                                    }) 

    
