# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015- Vertel AB (<http://www.vertel.se>).
#
#    This progrupdateam is free software: you can redistribute it and/or modify
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
import openerp.tools
import xmlrpclib
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class remote_database(models.Model):
	#_inherit = "account.analytic.account"
	_inherit = "res.users"

	@api.one
	def test(self, context=None):
		users = self.search_all_users('mail_azzar_se')
		self.user_amount = len(users)
		_logger.warn("The amount of users is::::::::::: %s" % self.user_amount)

	user_amount = fields.Integer(compute="test")
            
	def search_all_users(self, dbname):
		host = 'http://maggie.vertel.se'
		user   = 'admin'
		password = openerp.tools.config.get('passwd_passwd')

		try:
			sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' % host)           
			uid = sock_common.login(dbname, user, password)
			sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' % host)
		except xmlrpclib.Error as err:
			raise Warning(_("%s (server %s, db %s, user %s, pw %s)" % (err, host, dbname, user, password)))

		return sock.execute(dbname, uid, password, 'res.users', 'search', [])

    # def write(self):
    #     if not mainserver and self.isInstalled:      
    #         return self.sock.execute(self.passwd_dbname, self.uid, self.passwd_passwd, model, 'write', id, values)

    # def create(self, values):
    #     if not mainserver and self.isInstalled:
    #         return self.sock.execute(self.passwd_dbname, self.uid, self.passwd_passwd,model,'create', values)

    # def unlink(self, ids):
    #     if not mainserver and self.isInstalled:
    #         return self.sock.execute(self.passwd_dbname, self.uid, self.passwd_passwd, model, 'unlink',ids)	