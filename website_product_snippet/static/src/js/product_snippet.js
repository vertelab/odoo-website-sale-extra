var website = openerp.website;
website.add_template_file('/website_product_snippet/static/src/xml/product_snippet.xml');
var QWeb = openerp.qweb;
var template;

website.ProductSnippet = openerp.Widget.extend({
    //~ template: 'website_product_snippet.product_snippet',
    events: {},
    start: function () {
        var self = this;
        template = self.$el.append(QWeb.render('website_product_snippet.product_snippet'));
        return this._super();
    },
    destroy: function() {
        this._super();
    },
});

website.ready().done(function() {
    $(document).ready(function() {
        var ps = new website.ProductSnippet().appendTo($(document.body));
    });
});




/* option one: use snippet editor */
function product_change(product){
    if (product != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product
        }).done(function(data){
            $.each($(".individual_product"), function() {
                var src = $(this).find(".img").attr("data-cke-saved-src");
                if(src != undefined && !src.match("^data:")) {
                    $(this).find(".img").attr({
                        "data-cke-saved-src": "data:image/png;base64," + data['image'],
                        "src": "data:image/png;base64," + data['image']
                    });
                    $(this).find("h3").html("<span>" + data['name'] + "</span>");
                    $(this).find(".o_footer").find("small").html("<span>" + data['description'] + "</span>");
                    return false;
                }
            });
        });
    }
}

function get_products_by_category(categ_id){
    if (categ_id != "") {
        openerp.jsonRpc("/product_snippet/get_products_by_category", "call", {
            'categ_id': categ_id
        }).done(function(data){
            var counter = 1; // for some reason the first loop does not allowed to insert html
            $.each($(".products_by_category"), function() {
                if(counter == 2){
                    var product_content = '';
                    $.each(data['products'], function(key, info) {
                        template.find(".ps_product_name").html(data['products'][key]['name']);
                        template.find(".ps_product_image").attr({
                                'src': 'data:image/png;base64,' + data['products'][key]['image'],
                                'data-cke-saved-src': 'data:image/png;base64,' + data['products'][key]['image'],
                            });
                        template.find(".ps_product_description").html(data['products'][key]['description']);
                        product_content += template.prop('outerHTML');
                    });
                    $(this).find("h2").html(data['category']);
                    $(this).find(".products_by_category_content").html(product_content);
                }
                if(counter == 3){
                    return false;
                }
                counter ++;
            });
        });
    }
}

function get_products_by_partner(partner_id){
    if (partner_id != "") {
        openerp.jsonRpc("/product_snippet/get_products_by_partner", "call", {
            'partner_id': partner_id
        }).done(function(data){
            var counter = 1;
            $.each($(".products_by_partner"), function() {
                if(counter == 2){
                    var product_content = "";
                    $.each(data['products'], function(key, info) {
                        template.find(".ps_product_name").html(data['products'][key]['name']);
                        template.find(".ps_product_image").attr({
                                'src': 'data:image/png;base64,' + data['products'][key]['image'],
                                'data-cke-saved-src': 'data:image/png;base64,' + data['products'][key]['image'],
                            });
                        template.find(".ps_product_description").html(data['products'][key]['description']);
                        product_content += template.prop('outerHTML');
                    });
                    $(this).find("h2").html(data['partner']);
                    $(this).find(".products_by_partner_content").html(product_content);
                }
                if(counter == 3){
                    return false;
                }
                counter ++;
            });
        });
    }
}

function ind_col_change(col) {
    $(".individual_product").attr({
        "class": "individual_product col-md-" + col +" mb16 mt16"
    });
}

function ps_col_change(col) {
    $(".ps_outter").attr({
        "class": "ps_outter col-md-" + col
    });
}


/*
 * option two: use pure javascript
var current_element;

$(".individual_product").click(function(e) {
    $('#product_selector').css({'display': 'unset', "top": e.pageY, "left": e.pageX});
    $('#col_selector').css({'display': 'unset', "top": e.pageY + 35, "left": e.pageX});
    current_element = $(this);
});

$(document).ready(function() {
    $("body").append("<select id='product_selector'></select><select id='col_selector'><option value='3' onclick='col_change(3)'>col-3</option><option value='4' onclick='col_change(4)'>col-4</option><option value='6' onclick='col_change(6)'>col-6</option><option value='12' onclick='col_change(12)'>col-12</option></select>");
    openerp.jsonRpc("/product_snippet/get_products", "call", {
    }).done(function(data){
        $('#product_selector').append($("<option>", {
            value: "",
            text: "-- Choose a product --"
        }));
        $.each(data, function( key, value ) {
            $('#product_selector').append($("<option>", {
                value: key,
                text: value,
                onclick: "product_change(" + key + ")"
            }));
        });
    });
});

function product_change(product_id){
    if (product_id != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product_id
        }).done(function(data){
            current_element.find(".img").attr({
                "src": "data:image/png;base64," + data['image'],
            });
            current_element.find("h2").html("<span>" + data['name'] + "</span>");
            current_element.find("p").html("<span>" + data['description'] + "</span>");
        });
    }
}

function ind_col_change(col) {
    current_element.attr({
        "class": "individual_product col-md-" + col +" mb16 mt16"
    });
}
* */
