from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import get_pricelist
from openerp.tools.translate import _
from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class event_type(models.Model):
    _inherit = "event.type"

    link = fields.Char(string="URL")

class sale_order(models.Model):
    _inherit = "sale.order"

    driver_name = fields.Char(string = "Driver Name")
    parent_name = fields.Char(string = "Parent Name")
    birth_date = fields.Char(string = "Birth Date")
    length = fields.Char(string = "Length")
    other_info = fields.Char(string = "Other Info")

    def update_registration(self):
        registration = self.env['event.registration'].search([('origin', '=', self.name)])
        if registration:
            registration[0].write({
            'driver_name': self.driver_name,
            'birth_date': self.birth_date,
            'parent_name': self.parent_name,
            'length': self.length,
            'other_info': self.other_info
            })

class event_registration(models.Model):
    _inherit = "event.registration"

    driver_name = fields.Char(string = "Driver Name")
    parent_name = fields.Char(string = "Parent Name")
    birth_date = fields.Char(string = "Birth Date")
    length = fields.Char(string = "Length")
    other_info = fields.Char(string = "Other Info")


class website_gokart_form(http.Controller):

    @http.route(['/gokart/<model("event.event"):event>/register'], type='http', auth="public", website=True)
    def gokart_event(self, event, **post):
        pricelist_id = int(get_pricelist())
        if request.httprequest.method == 'POST':
            quantity = post.get('quantity', False)
            ticket = event.event_ticket_ids[0]
            order = request.website.sale_get_order(force_create=1)
            order.with_context(event_ticket_id=ticket.id)._cart_update(product_id=ticket.product_id.id, add_qty=quantity)
            order.write({
            'driver_name': post.get('driver_name'),
            'birth_date': post.get('birth_date'),
            'parent_name': post.get('parent_name'),
            'length': post.get('length'),
            'other_info': post.get('other_info')
            })
            return request.redirect("/shop/checkout")

        else:
            values = {
                'event': event.with_context(pricelist=pricelist_id),
                'main_object': event.with_context(pricelist=pricelist_id),
                'range': range,
            }
            return request.render('website_event.event_description_full', values)

    #~ @http.route(['/gokartserie/<model("event.event"):event>/register'], type='http', auth="public", website=True)
    #~ def gokartserie_event_register(self, event, **post):
        #~ pricelist_id = int(get_pricelist())
        #~ values = {
            #~ 'event': event.with_context(pricelist=pricelist_id),
            #~ 'main_object': event.with_context(pricelist=pricelist_id),
            #~ 'range': range,
        #~ }
        #~ return request.website.render("website_gokart_form.checkout_form_info", values)
