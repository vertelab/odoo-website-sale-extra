var website = openerp.website;
website.add_template_file('/website_product_snippet/static/src/xml/product_snippet.xml');

website.snippet.options.products_by_category = website.snippet.Option.extend({
    start: function () {
        var self = this;
        this._super();
        this.$el.find(".oe_products_by_category").on('click', function () {
            self.get_products_by_category($(this).attr("data-value"));
        });
        this.$el.find(".oe_ps_col_change").on('click', function () {
            self.ps_col_change($(this).attr("data-value"));
        });
    },
    get_products_by_category: function(categ_id){
        var self = this;
        if (categ_id != "") {
            openerp.jsonRpc("/product_snippet/get_products_by_category", "call", {
                'categ_id': categ_id
            }).done(function(data){
                self.$target.find(".oe_ps_title").html(data['category']);
                var product_content = '';
                $.each(data['products'], function(key, info) {
                    var content = openerp.qweb.render('product_snippet', {
                        'product_name': data['products'][key]['name'],
                        'product_image': "data:image/png;base64," + data['products'][key]['image'],
                        'product_description': data['products'][key]['description'],
                    });
                    product_content += content;
                });
                self.$target.find(".product_content").html(product_content);
            });
        }
    },
    ps_col_change: function(col) {
        var self = this;
        self.$target.find(".oe_ps_outer").attr({
            "class": "oe_ps_outer col-md-" + col
        });
    }
});

website.snippet.options.products_by_partner = website.snippet.Option.extend({
    start: function () {
        var self = this;
        this._super();
        this.$el.find(".oe_products_by_partner").on('click', function () {
            self.get_products_by_partner($(this).attr("data-value"));
        });
        this.$el.find(".oe_ps_col_change").on('click', function () {
            self.ps_col_change($(this).attr("data-value"));
        });
    },
    get_products_by_partner: function(partner_id){
        var self = this;
        if (partner_id != "") {
            openerp.jsonRpc("/product_snippet/get_products_by_partner", "call", {
                'partner_id': partner_id
            }).done(function(data){
                self.$target.find(".oe_ps_title").html(data['partner']);
                var product_content = '';
                $.each(data['products'], function(key, info) {
                    var content = openerp.qweb.render('product_snippet', {
                        'product_name': data['products'][key]['name'],
                        'product_image': "data:image/png;base64," + data['products'][key]['image'],
                        'product_description': data['products'][key]['description'],
                    });
                    product_content += content;
                });
                self.$target.find(".product_content").html(product_content);
            });
        }
    },
    ps_col_change: function(col) {
        var self = this;
        self.$target.find(".oe_ps_outer").attr({
            "class": "oe_ps_outer col-md-" + col
        });
    }
});

website.snippet.options.individual_product = website.snippet.Option.extend({
    start: function () {
        var self = this;
        this._super();
        this.$el.find(".oe_individual_product").on('click', function () {
            self.product_change($(this).attr("data-value"));
        });
        this.$el.find(".oe_ind_col_change").on('click', function () {
            self.ind_col_change($(this).attr("data-value"));
        });
    },
    product_change: function(product){
        var self = this;
        if (product != "") {
            openerp.jsonRpc("/product_snippet/product_change", "call", {
                'product': product
            }).done(function(data){
                var product_content = '';
                var content = openerp.qweb.render('product_snippet_individual', {
                    'product_name': data['name'],
                    'product_image': "data:image/png;base64," + data['image'],
                    'product_description': data['description'],
                });
                product_content += content;
                self.$target.find(".product_content").html(product_content);
            });
        }
    },
    ind_col_change: function(col) {
        var self = this;
        self.$target.attr({
            "class": "oe_individual_product col-md-" + col +" mb16 mt16"
        });
    }
});
