//~ (function () {
    //~ 'use strict';

    //~ var website = openerp.website;
    //~ website.add_template_file('/website/static/src/xml/website.xml');

    //~ website.MobilePreview = openerp.Widget.extend({
        //~ template: 'website.mobile_preview',
        //~ events: {
            //~ 'hidden.bs.modal': 'destroy'
        //~ },
        //~ start: function() {
            //~ if (!window.location.origin) { // fix for ie9
                //~ window.location.origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
            //~ }
            //~ document.getElementById("mobile-viewport").src = window.location.origin + window.location.pathname + window.location.search + "#mobile-preview";
            //~ this.$el.modal();
        //~ },
        //~ destroy: function() {
            //~ $('.modal-backdrop').remove();
            //~ this._super();
        //~ },
    //~ });

    //~ website.ready().done(function() {
        //~ $(document.body).on('click', 'a[data-action=show-mobile-preview]', function() {
            //~ new website.MobilePreview().appendTo($(document.body));
        //~ });
    //~ });

    function get_products(partner_id) {
        if (partner_id != "") {
            openerp.jsonRpc("/cavarosa/get_products", "call", {
                'partner_id': partner_id
            }).done(function(data){
                var counter = 1;
                $.each($(".cavarosa_products_by_supplier"), function() {
                    if(counter == 2){
                        var product_content = "";
                        $.each(data['products'], function(key, info) {
                            product_content += "<div class='crp_outter'><div class='crp_inner'><h3 class='text-center'>" + data['products'][key]['name'] +"</h3><img src='data:image/png;base64," + data['products'][key]['image'] + "' data-cke-saved-src='data:image/png;base64," + data['products'][key]['image'] + "'/><p>" + data['products'][key]['description'] + "</p></div></div>";
                        });
                        $(this).find(".cavarosa_products_by_supplier_title").html(data['supplier']);
                        $(this).find(".cavarosa_products_by_supplier_content").html(product_content);
                    }
                    if(counter == 3){
                        return false;
                    }
                    counter ++;
                });
            });
        }
    }

    function crp_col_change(col) {
        $(".crp_outter").attr({
            "class": "crp_outter col-md-" + col
        });
    }

//~ })();
