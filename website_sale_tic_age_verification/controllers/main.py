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

        age_limit = int(request.env['ir.config_parameter'].sudo().get_param(
            'website_sale_tic_age_verification.age_limit', 20))

        if order_sudo.partner_id.social_sec_nr_age == 0:
            raise ValidationError(
                _("Age could not be determined. Please ensure your social security number is correctly set."))
        if order_sudo.partner_id.social_sec_nr_age < age_limit:
            raise ValidationError(_(
                "You are not old enough to complete this purchase. You have to be at least %s years old."
            ) % age_limit)
            
        return super().shop_payment_transaction(order_id, access_token, **kwargs)
