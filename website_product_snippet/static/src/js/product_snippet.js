odoo.define('website.editor.snippets.options', function (require) {
'use strict';

var core = require('web.core');
var Dialog = require('web.Dialog');
var weWidgets = require('wysiwyg.widgets');
var options = require('web_editor.snippets.options');
var website = this.website;
var qweb = core.qweb;

    options.registry.product_snippet_options = options.Class.extend({
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
            self._rpc({
                route: "/product_snippet/get_products_by_category",
                params: {
                    categ_id: 'categ_id',
                    add_qty: 1,
                },
            }).then(function(data) {
                self.$target.find(".oe_ps_title").html(data['category']);
                var product_content = '';

                $.each(data['products'], function(key, info) {
                    var content = self.qweb.render('product_snippet', {
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


    // ps_col_change: function(col) {
    //     var self = this;
    //     self.$target.find(".oe_ps_outer").attr({
    //         "class": "oe_ps_outer col-md-" + col
    //     });
    // }
});
});

// options.registry.products_by_partner.include({
//     start: function () {
//         var self = this;
//         this._super();
//         this.$el.find(".oe_products_by_partner").on('click', function () {
//             self.get_products_by_partner($(this).attr("data-value"));
//         });
//         this.$el.find(".oe_ps_col_change").on('click', function () {
//             self.ps_col_change($(this).attr("data-value"));
//         });
//     },
//     get_products_by_partner: function(partner_id){
//         var self = this;
//         if (partner_id != "") {
//             self._rpc("/product_snippet/get_products_by_partner", "call", {
//                 'partner_id': partner_id
//             }).done(function(data){
//                 self.$target.find(".oe_ps_title").html(data['partner']);
//                 var product_content = '';
//                 $.each(data['products'], function(key, info) {
//                     var content = self.qweb.render('product_snippet', {
//                         'product_name': data['products'][key]['name'],
//                         'product_image': data['products'][key]['image'] != null ? ("data:image/png;base64," + data['products'][key]['image']) : '',
//                         'product_description': data['products'][key]['description'],
//                         'product_url': '/shop/product/' + data['products'][key],
//                     });
//                     product_content += content;
//                 });
//                 self.$target.find(".product_div").html(product_content);
//             });
//         }
//     },
//     ps_col_change: function(col) {
//         var self = this;
//         self.$target.find(".oe_ps_outer").attr({
//             "class": "oe_ps_outer col-md-" + col
//         });
//     }
// });

// options.registry.invidual_product.include({
//     start: function () {
//         var self = this;
//         this._super();
//         this.$el.find(".oe_individual_product").on('click', function () {
//             self.product_change($(this).attr("data-value"));
//         });
//         this.$el.find(".oe_ind_col_change").on('click', function () {
//             self.ind_col_change($(this).attr("data-value"));
//         });
//     },
//     product_change: function(product){
//         var self = this;
//         if (product != "") {
//             self._rpc("/product_snippet/product_change", "call", {
//                 'product': product
//             }).done(function(data){
//                 var product_content = '';
//                 var content = self.qweb.render('product_snippet_individual', {
//                     'product_name': data['name'],
//                     'product_image': "data:image/png;base64," + data['image'],
//                     'product_description': data['description'],
//                     'product_url': '/shop/product/' + data['id'],
//                 });
//                 product_content += content;
//                 self.$target.find(".product_div").html(product_content);
//             });
//         }
//     },
//     ind_col_change: function(col) {
//         var self = this;
//         self.$target.attr({
//             "class": "oe_individual_product col-md-" + col +" mb16 mt16"
//         });
//     }
// });
