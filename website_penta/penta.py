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
import openerp
import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp import http
from openerp.http import request
_logger = logging.getLogger(__name__)

class penta(http.Controller):

    @http.route(['/find_consultant'], type='http', auth='public', website=True)
    def find_consultant(self, **post):
        return request.website.render('website_penta.find_consultant', {})

    @http.route(['/work_with_us'], type='http', auth='public', website=True)
    def work_with_us(self, **post):
        return request.website.render('website_penta.work_with_us', {})
