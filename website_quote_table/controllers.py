# -*- coding: utf-8 -*-
from openerp import http

# class WebsiteQuoteTable(http.Controller):
#     @http.route('/website_quote_table/website_quote_table/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_quote_table/website_quote_table/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_quote_table.listing', {
#             'root': '/website_quote_table/website_quote_table',
#             'objects': http.request.env['website_quote_table.website_quote_table'].search([]),
#         })

#     @http.route('/website_quote_table/website_quote_table/objects/<model("website_quote_table.website_quote_table"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_quote_table.object', {
#             'object': obj
#         })