from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class UTMCampaign(models.Model):
    _inherit = 'utm.campaign'
    _mail_mass_mailing = _('Campaign')

    estimated_delivery = fields.Date(string='Estimated delivery')

    def action_clear_cart(self):
        sale_order_ids = self._get_sale_order(self.id)
        if sale_order_ids:
            sale_order_ids.write({'state': 'cancel'})

    def _get_sale_order(self, utm_id):
        sale_order_ids = self.env['sale.order'].search([
            ('campaign_id', '=', utm_id),
            ('state', 'in', ['draft', 'sent']),
            ('website_id', '!=', False)
        ])
        return sale_order_ids

    # def _clean_expired_cart_campaign(self):
    #     utm_campaign_ids = self.env['utm.campaign'].search([
    #         ('date_stop', '<', fields.Date.today()),
    #     ])
    #     for utm_campaign in utm_campaign_ids:
    #         sale_order_ids = self._get_sale_order(utm_campaign.id)
    #         if sale_order_ids:
    #             sale_order_ids.write({'state': 'cancel'})

