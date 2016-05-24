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
import logging
_logger = logging.getLogger(__name__)

class FloatConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.float'

    @api.model
    def precision(self, field, options={}):
        precision = options.get('precision')
        if precision == None:
            _, precision = field.digits or (None, None)
        return precision

#TODO: Implement precision on monetarty fields.
#~ class MonetaryConverter(models.AbstractModel):
    #~ _inherit = 'ir.qweb.field.monetary'
    #~ 
    #~ @api.model
    #~ def precision(self, field, display_currency, options={}):
        #~ precision = options.get('precision')
        #~ if precision != None:
            #~ precision = - precision
        #~ else:
            #~ precision = int(math.floor(math.log10(display_currency.rounding)))
        #~ return precision
    #~ 
    #~ @api.model
    #~ def record_to_html(self, field_name, record, options):
        #~ cr, uid, context = self._cr, self._uid, self._context
        #~ _logger.warn("\ncr:\t%s\nuid:\t%s\ncontext:\t%s\n" %(cr, uid, context))
        #~ if context is None:
            #~ context = {}
        #~ Currency = self.pool['res.currency']
        #~ display_currency = self.display_currency(cr, uid, options['display_currency'], options)
#~ 
        #~ # lang.format mandates a sprintf-style format. These formats are non-
        #~ # minimal (they have a default fixed precision instead), and
        #~ # lang.format will not set one by default. currency.round will not
        #~ # provide one either. So we need to generate a precision value
        #~ # (integer > 0) from the currency's rounding (a float generally < 1.0).
        #~ #
        #~ # The log10 of the rounding should be the number of digits involved if
        #~ # negative, if positive clamp to 0 digits and call it a day.
        #~ # nb: int() ~ floor(), we want nearest rounding instead
        #~ precision = self.precision(field_name, display_currency, options)
        #~ fmt = "%.{0}f".format(-precision if precision < 0 else 0)
#~ 
        #~ from_amount = record[field_name]
#~ 
        #~ if options.get('from_currency'):
            #~ from_currency = self.display_currency(cr, uid, options['from_currency'], options)
            #~ from_amount = Currency.compute(cr, uid, from_currency.id, display_currency.id, from_amount)
#~ 
        #~ lang_code = context.get('lang') or 'en_US'
        #~ lang = self.pool['res.lang']
        #~ formatted_amount = lang.format(cr, uid, [lang_code],
            #~ fmt, Currency.round(cr, uid, display_currency, from_amount),
            #~ grouping=True, monetary=True)
#~ 
        #~ pre = post = u''
        #~ if display_currency.position == 'before':
            #~ pre = u'{symbol}\N{NO-BREAK SPACE}'
        #~ else:
            #~ post = u'\N{NO-BREAK SPACE}{symbol}'
#~ 
        #~ return HTMLSafe(u'{pre}<span class="oe_currency_value">{0}</span>{post}'.format(
            #~ formatted_amount,
            #~ pre=pre, post=post,
        #~ ).format(
            #~ symbol=display_currency.symbol,
        #~ ))
