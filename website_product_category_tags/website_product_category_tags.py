# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class product_public_category(models.Model):
    _inherit = 'product.public.category'

    partner_tag_ids = fields.Many2many(comodel_name='res.partner.category', string='Partner Tags')


class product_template(models.Model):
    _inherit = 'product.template'

    @api.multi
    def product_visible(self, user_id):
        """
            A product is "visible" when its public category has common tags with the customer or customers company
            or doesnt have a public category with tags at all
        """
        self.ensure_one()

#        for c in self.public_categ_ids:
#             for t in  c.partner_tag_ids:
#                 t.id

        ptags = set([t.id for c in self.public_categ_ids for t in  c.partner_tag_ids])
        utags = set([c.id for c in user_id.partner_id.category_id])
        putags = set([c.id for c in user_id.partner_id.parent_id.category_id])
        if ptags:
            if user_id.partner_id.parent_id:
                if (ptags & utags) or (ptags & putags):
                    return True
                else:
                    return False
            else:
                if ptags  & utags:
                    return True
                else:
                    return False
        else:
            return True
