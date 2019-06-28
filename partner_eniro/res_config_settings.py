# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Register an account here: http://api.eniro.com/
    eniro_api_profile = fields.Char(string='Profile',help="Get your profile from Eniro http://api.eniro.com")
    eniro_api_key = fields.Char(string='Key',size=25,help="Get your Key from Eniro http://api.eniro.com")
        
    @api.model
    def get_values(self):
        res = super().get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update({
            'eniro_api_profile': get_param('eniro_api.profile'),
            'eniro_api_key': get_param('eniro_api.key'),
        })
        return res

    @api.multi
    def set_values(self):
        super().set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('eniro_api.profile', self.eniro_api_profile)
        set_param('eniro_api.key', self.eniro_api_key)
