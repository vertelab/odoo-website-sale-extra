# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class ir_rule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def init_records(self):
        product_comp_rule = self.env.ref('product.product_comp_rule')
        product_comp_rule.write({'domain_force': "['|',('company_ids','=',user.company_id.id),('company_ids','=',False)]"})


class product_template(models.Model):
    _inherit = 'product.template'

    company_ids = fields.Many2many(comodel_name='res.company', string='Companies')
