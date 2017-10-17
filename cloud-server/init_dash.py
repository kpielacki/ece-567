import dash
import dash_core_components as dcc
import dash_html_components as html


def user_dash(server):
    app = dash.Dash('User Portal', server=server,
                    url_base_pathname='/userportal', csrf_protect=False)

    # External CSS
    external_css = ["/assets/css/bootstrap.min.css"]
    for css in external_css:
        app.css.append_css({"external_url": css})

    external_scripts = ["/assets/vendor/jquery/jquery.min.js",
                        "/assets/vendor/bootstrap/js/bootstrap.min.js"]
    for script in external_scripts:
        app.scripts.append_script({"external_url": script})


    app.layout = html.Div([
        html.Div([
            html.H3('User Portal'),
        ], className="container")
    ], style={'padding-bottom': '20px'})

    return app
