# sale_order_block
Copy code to html for magic.

 <template id="index">
      <t t-call="website.layout">
     <div class="container" id="info-board" />
        <div class="row mt16" style=" margin-left: 0px; margin-right: 0px;">
          <!-- CURRENT JOBS -->
          <div class="col-md-4">
            <div class="panel-group" id="accordion">
              <div class="panel-heading text-center penta-block" style="background: #73AD21;">
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
                    <div class="panel-body">
                      <p t-field="active_order.website_short_description" />
                      <input type="hidden" name="redirect" value="/web?" />
                      <div class="clearfix oe_login_buttons">
                        <button type="submit" class="btn btn-primary">Intresseanmälan</button>
                        Om inloggad, annars redirect login.
                      </div>
                    </div>
                  </div>
                </t>
              </div>
            </div>
          </div>
          <!-- /CURRENT JOBS -->
          <!-- LOGIN FORM column width added -->
          <div class="col-md-4">
            <div class="panel panel-login">
              <div class="panel-heading text-center penta-block">
                <div class="col-xs-6">
                  <a href="#" class="active" id="login-form-link">Logga in</a>
                </div>
                <div class="col-xs-6">
                  <a href="#" class ="" id="register-form-link">Intresseanmälan</a>
                </div>
              </div>
              <div class="panel-body">
                <form class="oe_login_form active" id="login-form" role="form" action="/web/login" method="post" onsubmit="this.action = this.action + location.hash">
                  <div class="form-group field-login">
                    <label for="login" class="control-label">Email</label>
                    <input type="text" name="login" id="login" class="form-control" required="required" />
                  </div>
                  <div class="form-group field-password">
                    <label for="password" class="control-label">Password</label>
                    <input type="password" name="password" id="password" class="form-control" required="required" />
                  </div>
                  <input type="hidden" name="redirect" value="/web?" />
                  <div class="clearfix oe_login_buttons">
                    <button type="submit" class="btn btn-primary">Log in</button>
                  </div>
                </form>
                <form class="oe_login_form" role="form" id="register-form" style="display:none">
                  <div class="form-group field-login">
                    <label for="name" class="control-label">Namn</label>
                    <input type="text" name="name" id="name" class="form-control" required="required" />
                  </div>
                  <div class="form-group field-login">
                    <label for="login" class="control-label">Email</label>
                    <input type="text" name="login" id="login" class="form-control" required="required" />
                  </div>
                  <div class="form-group field-password">
                    <label for="password" class="control-label">Password</label>
                    <input type="password" name="password" id="password" class="form-control" required="required" />
                  </div>
                  <input type="hidden" name="redirect" value="/web?" />
                  <div class="clearfix oe_login_buttons">
                    <button type="submit" class="btn btn-primary">Log in</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <!-- /LOGIN FORM -->
          <!-- HITTA KONSULT -->
          <div class="col-md-4">
            <div class="btn-pref btn-group btn-group-justified btn-group-lg" role="group" aria-label="...">
              <div class="btn-group" role="group">
                <button type="button" id="stars" class="btn btn-primary" href="#tab1" data-toggle="tab">
                  <span class="glyphicon glyphicon-star" aria-hidden="true" />
                  <div class="hidden-xs-up">Konsulter</div>
                </button>
              </div>
              <div class="btn-group" role="group">
                <button type="button" id="favorites" class="btn btn-default" href="#tab2" data-toggle="tab">
                  <span class="glyphicon glyphicon-heart" aria-hidden="true" />
                  <div class="hidden-xs-up">Registrera uppdrag</div>
                </button>
              </div>
              <div class="btn-group" role="group">
                <button type="button" id="following" class="btn btn-default" href="#tab3" data-toggle="tab">
                  <span class="glyphicon glyphicon-user" aria-hidden="true" />
                  <div class="hidden-xs-up">Skapa inloggning</div>
                </button>
              </div>
            </div>
            <div class="well">
              <div class="tab-content">
                <div class="tab-pane fade in active" id="tab1">
                  <h3>våra konsulter</h3>
                </div>
                <div class="tab-pane fade in" id="tab2">
                  <h3>Registrera uppdrag</h3>
                </div>
                <div class="tab-pane fade in" id="tab3">
                  <h3>Skapa inloggning</h3>
                </div>
              </div>
            </div>
          </div>
          <!-- /HITTA KONSULT-->
        </div>
      </t>
      <script>// Login form
        $(document).ready(function() {
        $('#login-form-link').click(function(e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
        });
        $('#register-form-link').click(function(e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
        });
        
        });
        // 3 tab handler
        $(document).ready(function() {
        $(".btn-pref .btn").click(function () {
        $(".btn-pref .btn").removeClass("btn-primary").addClass("btn-default");
        // $(".tab").addClass("active"); // instead of this do the below      
        $(this).removeClass("btn-default").addClass("btn-primary");   
        });
        });</script>
    </template>
