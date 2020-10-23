var website = odoo.website;
website.add_template_file('/website_sale_cavarosa/static/src/xml/snippets.xml');

var core = require('web.core');
var Dialog = require('web.Dialog');
var weWidgets = require('wysiwyg.widgets');
var options = require('web_editor.snippets.options');
var website = this.website;
var qweb = core.qweb;

website.snippet.options.current_campaign_navigator_option = website.snippet.Option.extend({
    start: function () {
        var self = this;
        this._super();
        this.$el.find(".oe_get_campaign").on('click', function () {
            self.get_campaign($(this).attr("data-value"));
        });
    },
    get_campaign: function(campaign_id){
        if (campaign_id != '') {
            var self = this;
            self._rpc("/snippet/get_campaign", "call", {
                'campaign_id': campaign_id,
            }).then(function(data){
                var supplier_content = '';
                $.each(data, function(key, info) {
                    var content = qweb.render('supplier_content', {
                        'supplier_url': data[key]['supplier_url'],
                        'supplier_name': data[key]['supplier_name'],
                    });
                    content = content.replace("image_url", data[key]['supplier_image']);
                    supplier_content += content;
                });
                self.$target.find(".supplier_content").html(supplier_content + "<t t-esc='user_id'/>");
            });
        }
    }
});
