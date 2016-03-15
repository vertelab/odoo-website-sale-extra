<template id="index">
      <t t-call="website.layout">
        <div class="container" id="info-board">
          <div class="text-field col-md-8 mt32" id="ingresstext">
            <p class="text-center">
              <h4>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                ulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                deserunt mollit anim id est laborum.
              </h4>
            </p>
          </div>
          <div class="col-md-6">
            <div class="panel panel-login">
              <div class="panel-heading text-center penta-block">
                <div class="col-xs-4">
                  <button type="button" class="btn btn-primary" id="intressent-form-link">Intresseanmälan</button>
                </div>
                <div class="col-xs-4">
                  <button type="button" class="btn btn-primary" id="login-form-link">Logga in</button>
                </div>
                <div class="col-xs-4">
                  <button type="button" class="btn btn-primary" id="register-form-link">Skapa konto</button>
                </div>
              </div>
              <div class="panel-body">
                <form class="oe_register_form active" id="intressent-form" role="form" action="" method="post" onsubmit="">
                  <p class="mt16">Lämna dina uppgifter så berättar vi mer.</p>
                  <div class="col-xs-6">
                    <div class="form-group">
                      <input placeholder="Namn" type="text" name="name" id="name" class="form-control" required="required" />
                    </div>
                    <div class="form-group">
                      <input placeholder="Epost" type="text" name="email" id="email" class="form-control" required="required" />
                    </div>
                    <div class="form-group">
                      <input placeholder="Telefonnummer" type="text" name="phonenumber" id="phonenumber" class="form-control" required="required" />
                    </div>
                    <div class="clearfix oe_login_buttons">
                      <button type="submit" class="btn btn-primary">Skicka</button>
                    </div>
                  </div>
                  <div class="col-xs-4">
                    <textarea name="textarea" style="resize: none;" type="text" placeholder="Meddelande (valfritt)" rows="8" cols="26" />
                  </div>
                </form>
                <form class="oe_register_form" id="login-form" role="form" action="" method="post" onsubmit="" style="display:none">
                  <br />
                  <div class="col-xs-6">
                    <div class="form-group">
                      <input placeholder="Login" type="text" name="login" id="login" class="form-control" required="required" />
                    </div>
                    <div class="form-group">
                      <input placeholder="Lösenord" type="password" name="password" id="password" class="form-control" required="required" />
                    </div>
                    <div class="clearfix oe_login_buttons">
                      <button type="submit" class="btn btn-primary">Skicka</button>
                    </div>
                  </div>
                </form>
                <form class="oe_register_form" id="register-form" role="form" action="" method="post" onsubmit="" style="display:none">
                  <br />
                  <div class="col-xs-6">
                    <div class="form-group">
                      <input placeholder="Namn" type="text" name="name" id="name" class="form-control" required="required" />
                    </div>
                    <div class="clearfix oe_login_buttons">
                      <button type="submit" class="btn btn-primary">Skicka</button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </t>
      <script>
        function testLoginForm() {
        var name = document.getElementById("name").value;
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phonenumber").value;
        var texten = "name: " + name + "\nemail: " + email + "\nphone: " + phone;
        alert(texten);
        }
        
        $(document).ready(function() {
        $('#intressent-form-link').click(function(e) {
        $("#intressent-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
        });
        $('#login-form-link').click(function(e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#intressent-form").fadeOut(100);
        $('#intressent-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
        });
        
        });
      </script>
    </template>
    <!-- SENASTE UPPDRAGEN -->
    <template id="senaste_uppdragen">
      <t t-call="website.layout">
        <div class="container" id="info-board">
          <div class="row mt16">
            <div class="col-md-4">
              <div class="panel-group" id="accordion">
                <div class="panel-heading text-center penta-block">
                  <h4 style="margin: 0">
                    <span>Senaste uppdragen</span>
                  </h4>
                </div>
                <div class="panel panel-default">
                  <t t-foreach="request.env['sale.order'].sudo().search([('website_published','=',True)],limit=4).sorted(key=lambda r: r.partner_id.name)" t-as="active_order">
                    <div class="panel-heading">
                      <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion" t-att-href="'#%s' %active_order.name" t-field="active_order.website_subject" />
                      </h4>
                    </div>
                    <div t-att-id="'%s'%active_order.name" class="panel-collapse collapse">
                      <div class="panel-body" style="background: #FFFFFF;">
                        <div class="row">
                          <span>
                            <div class="col-sm-4">
                              Start
                              <p t-esc='active_order.date_start' />
                            </div>
                            <div class="col-sm-4">
                              Stop
                              <p t-esc='active_order.date_stop' />
                            </div>
                          </span>
                        </div>
                        <div class='row'>
                          <div class="col-sm-8">
                              <p style='padding:2px'  t-esc="'Omfattning: %.2f %s' %(active_order.qty, active_order.uom_id.name)"/>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-sm-2">Plats:</div>
                          <t t-foreach='active_order.location_ids' t-as='loc'>
                            <p style='padding: 2px' class='label label-default' t-esc='loc.name' />
                          </t>
                        </div>
                        <div class="row">
                          <div class="col-sm-2">Språk:</div>
                          <t t-foreach='active_order.language_ids' t-as='l'>
                            <p style='padding: 2px' class='label label-default' t-esc='l.name' />
                          </t>
                        </div>
                        <div class="row">
                          <div class="col-sm-2">Skills:</div>
                          <div class="col-sm-6">
                            <t t-set='skill_desc' t-value='active_order.skill_ids._fields["level"].get_description(active_order.env)["selection"]' />
                            <t t-foreach="active_order.skill_ids" t-as='s'>
                              <t t-set='level' t-value='[l[1] for l in skill_desc if l[0] == s.level][0]' />
                              <p style='padding:2px' class="label label-default" t-esc="'%s (%s)' % (s.categ_id.name, level)" />
                            </t>
                          </div>
                        </div>
                        
                        <p t-field="active_order.website_description" />
                        <div class="clearfix oe_login_buttons">
                          <a t-att-href="'/so/%s/interest'%active_order.id">
                            <button type="submit" class="btn btn-primary" groups="base.group_user">Intresseanmälan</button>
                          </a>
                        </div>
                        <div class="clearfix oe_login_buttons">
                          <a t-att-href="'login/redirect=%s'%active_order.name">
                            <button type="submit" class="btn btn-primary" groups="base.group_public">Logga in</button>
                          </a>
                        </div>
                      </div>
                    </div>
                  </t>
                </div>
              </div>
            </div>
          </div>
        </div>
      </t>
    </template>
