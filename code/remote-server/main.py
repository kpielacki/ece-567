import argparse
from admin_app_config import admin
from admin_views import add_admin_views


from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly_app import app
from dashboards import (user_dash, business_dash)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # Add routes to new dashboards here
    if pathname == '/userdash/':
        return user_dash.layout
    elif pathname == '/businessdash/':
        return business_dash.layout
    else:
        return "404"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server run options')
    parser.add_argument('port', type=int)
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()
    
    with app.server.app_context():
        add_admin_views(admin, app)
        app.run_server(host='0.0.0.0', port=args.port, debug=args.debug)
