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
from openerp.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class partner_image_wizard(models.TransientModel):
    _name = 'res.partner.image.wizard'
    
    image = fields.Binary('Image', required=True)
    partner_ids = fields.One2many(comodel_name='res.partner', string='Partners', compute='dummy_mcdummyface')

    @api.one
    def dummy_mcdummyface(self):
        ids = self.env.context.get('active_ids')
        if ids:
            self.partner_ids = self.env['res.partner'].browse(ids)
            _logger.warn('WTF? %s' % self.partner_ids)
        else:
            self.partner_ids = self.env['res.partner'].browse()
    
    @api.one
    def change_image(self):
        self.partner_ids.write({'image': self.image})

