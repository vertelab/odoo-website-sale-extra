from odoo import _, api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    age_limit = fields.Integer(
        string='Age Limit', config_parameter='website_sale_tic_age_verification.age_limit', default=20
    )

