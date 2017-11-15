from admin_app_config import db
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from models import (UserLocation, UserSteps, HazardSummary, HazardLocation)
import numpy as np


def user_dash(server):
    USER_ID_TEMP = 1
    MAP_ACCESS_TOKEN = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMD' \
                       'AxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
    HEALTH_DROPDOWN_OPTIONS = ['Step Count', 'Calories']
    HEALTH_DAYS_OPTIONS = (
        ('Past Week', '7'),
        ('Past Month', '31'),
        ('Past Year', '365'),
    )
    MAP_DAYS_OPTIONS = HEALTH_DAYS_OPTIONS
    query = db.session.query(
        HazardLocation.hazard_category.distinct().label('s'))
    hazard_options = [{'label': row.s, 'value': row.s}
                      for row in query.all()]

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
            html.H1('User Portal'),
            html.Div([
                html.H3('Activity Trend'),
                dcc.Dropdown(
                    id='health-days-dropdown',
                    options=[{'label': label, 'value': value}
                             for label, value in HEALTH_DAYS_OPTIONS],
                    value=HEALTH_DAYS_OPTIONS[1][1]
                ),
                dcc.Dropdown(
                    id='health-dropdown',
                    options=[{'label': s, 'value': s}
                             for s in HEALTH_DROPDOWN_OPTIONS],
                    value=HEALTH_DROPDOWN_OPTIONS[0]
                ),
                dcc.Graph(
                    id='health-trend',
                    style={
                        'max-height': '300px'
                    }
                ),
                html.H3('Health Hazards'),
                dcc.Dropdown(
                    id='map-days',
                    options=[{'label': label, 'value': value}
                             for label, value in MAP_DAYS_OPTIONS],
                    value=MAP_DAYS_OPTIONS[1][1]
                ),
                dcc.Dropdown(
                    id='hazard-dropdown',
                    options=hazard_options,
                    value=hazard_options[0]['value']
                ),
                dcc.Graph(id='map-graph'),
                html.Div([], id='about-hazard'),
            ]),
        ], className="container")
    ], style={'padding-bottom': '20px'})

    def get_user_locations(date):
        result = db.session.query(UserLocation) \
            .filter(UserLocation.user_id == USER_ID_TEMP) \
            .filter(UserLocation.date >= date).all()

        user_dts = []
        user_latitudes = []
        user_longitudes= []
        for r in result:
            user_dts.append(r.date)
            user_latitudes.append(r.latitude)
            user_longitudes.append(r.longitude)
        init_lat = np.mean(user_latitudes)
        init_long = np.mean(user_longitudes)

        return Scattermapbox(
            lat=user_latitudes,
            lon=user_longitudes,
            text=user_dts,
            mode='markers',
            hoverinfo="lat+lon+text",
            marker=Marker(
                color='blue',
                opacity=40,
                size=20,
            ),
        ), init_lat, init_long


    def get_hazard_locations(value):
        result = db.session.query(HazardLocation) \
            .filter(HazardLocation.hazard_category == value).all()
        names = []
        latitudes = []
        longitudes= []
        for r in result:
            names.append(r.place_name)
            latitudes.append(r.latitude)
            longitudes.append(r.longitude)

        return Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            text=names,
            mode='markers',
            hoverinfo="lat+lon+text",
            marker=Marker(
                color='red',
                opacity='0.2',
                size=100,
            ),
        )

    @app.callback(Output("map-graph", "figure"),
                  [Input('map-days', 'value'),
                   Input('hazard-dropdown', 'value')])
    def update_graph(day_str, value):
        try:
            day_cnt = int(day_str)
        except:
            return "Invalid day input"

        if day_cnt < 1 or day_cnt > 365:
            return "Invalid day count value"

        try:
            date_from = datetime.date.today() - datetime.timedelta(days=day_cnt)  
            user_data, init_lat, init_long = get_user_locations(date_from)
            hazard_data = get_hazard_locations(value)
        except:
            return "Map Data Unavailable"

        bearing = 0
        zoom = 12.0
        return go.Figure(
            data=Data([user_data, hazard_data]),
            layout=Layout(
                autosize=True,
                height=499,
                margin=Margin(l=0, r=0, t=10, b=10),
                showlegend=False,
                mapbox=dict(
                    accesstoken=MAP_ACCESS_TOKEN,
                    center=dict(
                        lat=init_lat,
                        lon=init_long
                    ),
                    style='dark',
                    bearing=bearing,
                    zoom=zoom
                ),
            )
        )

    def get_recent_activity(value, day_cnt, user_id):
        date_from = datetime.date.today() - datetime.timedelta(days=day_cnt)  
        result = db.session.query(UserSteps) \
            .filter(UserSteps.user_id == user_id) \
            .filter(UserSteps.date >= date_from) \
            .order_by(UserSteps.date.desc()).all()
        xs = []
        ys = []
        for r in result:
            xs.append(r.date)
            ys.append(r.step_count)
        return xs, ys

    @app.callback(Output("health-trend", "figure"),
                  [Input('health-days-dropdown', 'value'),
                   Input('health-dropdown', 'value')])
    def update_graph(days_value, value):
        # Prevent request modification
        try:
            day_cnt = int(days_value)
        except:
            return "Invalid Day Selection"

        # Prevent larger queries
        if day_cnt < 1 or day_cnt > 365:
            return "Invalid Day Selection"

        try:
            xs, ys = get_recent_activity(value, day_cnt, USER_ID_TEMP)
        except:
            return "User Data Unavailable"

        return {
            'data': [{
                'x': xs,
                'y': ys
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }

    @app.callback(Output("about-hazard", "children"),
                  [Input('hazard-dropdown', 'value')])
    def update_info(value):
        result = db.session.query(HazardSummary) \
            .filter(HazardSummary.hazard_category == value).first()

        # Return message if no summary available
        if result is None:
            return html.P('Information will be available in the future.')

        if result.source is None:
            src_content = html.P("Source unavailable")
        else:
            src_content = html.A(
                'Source',
                id='hazard-source',
                href=result.source, target="_blank"
            )

        return html.Div([
            html.H4('About {}'.format(value)),
            src_content,
            html.P(result.summary)
        ])

    return app
