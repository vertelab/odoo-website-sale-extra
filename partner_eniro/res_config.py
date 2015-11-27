# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class partner_eniro_configuration(models.TransientModel):
    _inherit = 'base.config.settings'
        
    def get_default_eniro(self,cr,uid,ids,context):
        return {
            'eniro_api_profile': self.pool.get('ir.config_parameter').get_param(cr,uid,'eniro_api_profile', ''),
            'eniro_api_key':     self.pool.get('ir.config_parameter').get_param(cr,uid,'eniro_api_key', ''),
        }
    
    def set_eniro(self,cr,uid,ids,context):
        obj = self.pool.get('base.config.settings').browse(cr,uid,ids[0])
        self.pool.get('ir.config_parameter').set_param(cr,uid,'eniro_api_profile',obj.eniro_api_profile or '')
        self.pool.get('ir.config_parameter').set_param(cr,uid,'eniro_api_key', obj.eniro_api_key or '')

    eniro_api_profile = fields.Char(string='Profile',help="Get your profile from Eniro http://api.eniro.com")
    eniro_api_key = fields.Char(string='Key    ',size=25,help="Get your Key from Eniro http://api.eniro.com")
