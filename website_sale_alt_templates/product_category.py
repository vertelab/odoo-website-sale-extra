from openerp import api, fields, models, _

from openerp.addons.website_sale.controllers.main import table_compute

class product_public_category(models.Model):
    _inherit = 'product.public.category'
    
    @api.model
    def calculate_grid(self, products):
        return table_compute().process(products)
