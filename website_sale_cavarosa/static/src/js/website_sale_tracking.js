odoo.define('website_sale_cavarosa.tracking', function (require) {

    var publicWidget = require('web.public.widget');
    var website_tracking = require('website_sale.tracking')

publicWidget.registry.websiteSaleTracking = publicWidget.Widget.extend({
        _onAddProductIntoCart: function () {
            console.log("_onAddProductIntoCart")
            var productID = this.$('input[name="product_id"]').attr('value');
//            var campaign_id = this.$('input[name="campaign_id"]').attr('value');
            this._vpv('/stats/ecom/product_add_to_cart/' + productID);
        },
    })

})