# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import PaymentPortal

class PaymentPortalAgeVerification(PaymentPortal):

    @http.route()
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        order_sudo = self._document_check_access('sale.order', order_id, access_token)
        
        if order_sudo and order_sudo.partner_id.tic_identity_status != 'verified':
            raise ValidationError(_("Age verification is required to complete this purchase."))
            
        return super().shop_payment_transaction(order_id, access_token, **kwargs)
