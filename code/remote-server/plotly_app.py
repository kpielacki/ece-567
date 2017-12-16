from admin_app_config import (server, admin)
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash('Health Dashboards', server=server,
                url_base_pathname='/dashboards', csrf_protect=False)

# External CSS
external_css = ["/assets/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_scripts = ["/assets/vendor/jquery/jquery.min.js",
                    "/assets/vendor/bootstrap/js/bootstrap.min.js"]
for script in external_scripts:
    app.scripts.append_script({"external_url": script})
app.config.supress_callback_exceptions = True
