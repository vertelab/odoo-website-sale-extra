odoo.define('website_product_snippet.products', function (require){
	
var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');
var weWidgets = require('wysiwyg.widgets');
var options = require('web_editor.snippets.options');
var website = this.website;
var qweb = core.qweb;

options.registry.products_by_category = options.Class.extend({
    selector : '.oe_products_by_category',

    start: function () {
        var self = this;
        var div_height = 0;
        self._super();
        console.log("hej");
        self.$el.find(".oe_products_by_category").on('click', function () {
            self.get_products_by_category($(this).attr("data-value"));
        });
        console.log(this.$target.find(".oe_products_by_category"));
        self.$el.find(".oe_ps_col_change").on('click', function () {
            self.ps_col_change($(this).attr("data-value"));
        });
    },

    get_products_by_category: function(categ_id) {
            var self = this;
             if (categ_id != "") {
            ajax._rpc({
                route: "/product_snippet/get_products_by_category",
                params: {
                    categ_id: 'categ_id',
                    add_qty: 1,
                },
            }).then(function(data) {
                self.$el.find(".oe_ps_title").html(data['category']);
                var product_content = '';

                $.each(data['products'], function(key, info) {
                    self.$target.append($('<div/>', {class: 'col-md-6 offset-md-3'})
                    .append($('<div/>', {
                        class: 'alert alert-warning alert-dismissible text-center',
                        text: _t("No blog post was found. Make sure your posts are published."),
                    })));

                    var content = qweb.render('website_product_snippets.website_product_category', {
                        'product_name': data['products'][key]['name'],
                        // 'product_image': data['products'][key]['image'] != null ? ("data:image/png;base64," + data['products'][key]['image']) : '',
                        'product_description': data['products'][key]['description'],
                        'product_url': '/shop/product/' + key,
                    });
                    product_content += content;
                });

                self.$el.find(".product_div").html(product_content);
            
            });
        }
    }


});

});