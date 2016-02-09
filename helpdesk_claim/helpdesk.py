# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)

class crm_helpdesk(models.Model):
    _inherit ='crm.helpdesk'
    
    claim_id = fields.Many2one(comodel_name="crm.claim", string="Claim")
    
    @api.one
    def create_claim(self):
        if (not self.claim_id):
            claim_id = self.env['crm.claim'].create({
                'name': self.name,
                'user_id': self.user_id.id,
                'partner_id': self.partner_id.id, 
                'partner_phone': self.partner_id.phone,
                'email_from': self.email_from,
                'priority': self.priority,
                'helpdesk_id': self.id
            })
            self.claim_id = claim_id.id
            partner_id = self.env['res.users'].browse(self._uid).partner_id.id
            self.env['mail.message'].create({
                'body': _("Escalated to new claim with id %s" % claim_id.id),
                'subject': 'Escalated to claim',
                'author_id': partner_id,
                'res_id': self.id,
                'model': self._name,
                'type': 'notification',
            })

class crm_claim(models.Model):
    _inherit ='crm.claim'
    
    helpdesk_id = fields.Many2one(comodel_name="crm.helpdesk", string="Helpdesk request")
