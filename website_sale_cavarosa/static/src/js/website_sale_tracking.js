odoo.define('website_sale_cavarosa.tracking', function (require) {

    var publicWidget = require('web.public.widget');
    var website_tracking = require('website_sale.tracking')
    var PaymentForm = require('payment.payment_form')


    publicWidget.registry.websiteSaleTrackingC = publicWidget.Widget.extend({
        events: {
            'click #proceed_to_checkout': '_ProceedToCheckout',
        },

        _onAddProductIntoCart: function () {
            console.log("_onAddProductIntoCart")
            var productID = this.$('input[name="product_id"]').attr('value');
//            var campaign_id = this.$('input[name="campaign_id"]').attr('value');
            this._vpv('/stats/ecom/product_add_to_cart/' + productID);
        },


        _ProceedToCheckout: function (ev) {
            console.log("_ProceedToCheckout")
            ev.preventDefault()
            alert("This is not good")
        },
    })

    PaymentForm.extend({
        onSubmit: function(ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var button = $(ev.target).find('*[type="submit"]')[0]
            if (button.id === 'o_payment_form_pay') {
                return this.payEvent(ev);
            } else if (button.id === 'o_payment_form_add_pm') {
                return this.addPmEvent(ev);
            }
            return;
        },

    })

})

