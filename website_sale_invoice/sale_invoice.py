from openerp import models, fields, api, _
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale
import logging

_logger = logging.getLogger(__name__)

class website_sale(http.Controller):
    _inherit = 'website.sale'

    def checkout_form_save(self, checkout):
        res = super(website_sale,self).checkout_form_save()
        _logger.warn('----------- %s' %res)

        #~ cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        #~ order = request.website.sale_get_order(force_create=1, context=context)

        #~ orm_partner = registry.get('res.partner')
        #~ orm_user = registry.get('res.users')
        #~ order_obj = request.registry.get('sale.order')

        #~ partner_lang = request.lang if request.lang in [lang.code for lang in request.website.language_ids] else None

        #~ billing_info = {'customer': True}
        #~ if partner_lang:
            #~ billing_info['lang'] = partner_lang
        #~ billing_info.update(self.checkout_parse('billing', checkout, True))

        #~ # set partner_id
        #~ partner_id = None
        #~ if request.uid != request.website.user_id.id:
            #~ partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        #~ elif order.partner_id:
            #~ user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID,
                #~ [("partner_id", "=", order.partner_id.id)], context=dict(context or {}, active_test=False))
            #~ if not user_ids or request.website.user_id.id not in user_ids:
                #~ partner_id = order.partner_id.id

        #~ # save partner informations
        #~ if partner_id and request.website.partner_id.id != partner_id:
            #~ orm_partner.write(cr, SUPERUSER_ID, [partner_id], billing_info, context=context)
        #~ else:
            #~ # create partner
            #~ partner_id = orm_partner.create(cr, SUPERUSER_ID, billing_info, context=context)

        #~ # create a new invoice partner
        #~ if checkout.get('invoice_id') == -1:
            #~ shipping_info = self._get_shipping_info(checkout)
            #~ if partner_lang:
                #~ shipping_info['lang'] = partner_lang
            #~ shipping_info['parent_id'] = partner_id
            #~ checkout['shipping_id'] = orm_partner.create(cr, SUPERUSER_ID, shipping_info, context)

        #~ order_info = {
            #~ 'partner_id': partner_id,
            #~ 'message_follower_ids': [(4, partner_id), (3, request.website.partner_id.id)],
            #~ 'partner_invoice_id': partner_id,
        #~ }
        #~ order_info.update(order_obj.onchange_partner_id(cr, SUPERUSER_ID, [], partner_id, context=context)['value'])
        #~ address_change = order_obj.onchange_delivery_id(cr, SUPERUSER_ID, [], order.company_id.id, partner_id,
                                                        #~ checkout.get('shipping_id'), None, context=context)['value']
        #~ order_info.update(address_change)
        #~ if address_change.get('fiscal_position'):
            #~ fiscal_update = order_obj.onchange_fiscal_position(cr, SUPERUSER_ID, [], address_change['fiscal_position'],
                                                               #~ [(4, l.id) for l in order.order_line], context=None)['value']
            #~ order_info.update(fiscal_update)

        #~ order_info.pop('user_id')
        #~ order_info.update(partner_shipping_id=checkout.get('shipping_id') or partner_id)

        #~ order_obj.write(cr, SUPERUSER_ID, [order.id], order_info, context=context)
