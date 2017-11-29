from plotly_app import app
from admin_app_config import db
from utils import vicinity_rate


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import (Input, Output, State, Event)
import datetime
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from models import (User, UserLocation, UserSteps, HazardSummary,
                    HazardLocation)
import numpy as np


with app.server.app_context():

    GOOD_GLYPH = html.Span(className='glyphicon glyphicon-ok',
                           style={'color': 'green'})
    WARN_GLYPH = html.Span(className='glyphicon glyphicon-warning-sign',
                           style={'color': 'orange'})
    BAD_GLYPH = html.Span(className='glyphicon glyphicon-remove',
                           style={'color': 'red'})


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
    MILE_OPTIONS = (
        ('0.1 Miles', '0.1'),
        ('0.5 Miles', '0.5'),
        ('1 Miles', '1'),
        ('5 Miles', '5'),
        ('10 Miles', '10'),
        ('25 Miles', '25'),
    )
    query = db.session.query(
        HazardLocation.hazard_category.distinct().label('s'))
    hazard_options = [{'label': row.s, 'value': row.s}
                      for row in query.all()]
    
    layout = html.Div([
        html.Div([
            html.H1('User Portal'),
            html.Div([
                html.H3('Activity Trend'),
                html.P('Time Interval', className='label'),
                dcc.Dropdown(
                    id='health-days-dropdown',
                    options=[{'label': label, 'value': value}
                             for label, value in HEALTH_DAYS_OPTIONS],
                    value=HEALTH_DAYS_OPTIONS[1][1]
                ),
                html.P('Trend Type', className='label'),
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
                html.P('Time Period', className='label'),
                dcc.Dropdown(
                    id='map-days',
                    options=[{'label': label, 'value': value}
                             for label, value in MAP_DAYS_OPTIONS],
                    value=MAP_DAYS_OPTIONS[1][1]
                ),
                html.P('Hazard Category', className='label'),
                dcc.Dropdown(
                    id='hazard-dropdown',
                    options=hazard_options,
                    value=hazard_options[0]['value']
                ),
                html.P('Distance', className='label'),
                dcc.Dropdown(
                    id='mile-dropdown',
                    options=[{'label': label, 'value': value}
                             for label, value in MILE_OPTIONS],
                    value=MILE_OPTIONS[0][1]
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
    
    def get_vicinity_summary(uid, hazard_type, day_cnt, mile_thresh):
        date_from = datetime.date.today() - datetime.timedelta(days=day_cnt) 
        results = db.session.query(UserLocation) \
            .filter(UserLocation.user_id == uid) \
            .filter(UserLocation.date >= date_from).all()
        user_points = [(r.latitude, r.longitude) for r in results]

        results = db.session.query(HazardLocation) \
            .filter(HazardLocation.hazard_category == hazard_type).all()
        src_points = [(r.latitude, r.longitude) for r in results]

        return vicinity_rate(src_points, user_points, mile_thresh)

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

    def steps_to_calories(step_cnt, weight):
        """Calculates the calories burned from total steps.
        https://www.livestrong.com/article/238020-how-to-convert-pedometer-steps-to-calories/

        :step_cnt (Integer): Number of steps.

        Returns (Integer): Number of calories burned.
        """
        return (float(0.57 * weight) / 2200) * step_cnt
    
    def get_recent_activity(value, day_cnt, user_id, trend_type):
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

        if trend_type.strip() == 'Calories':
            result = db.session.query(User).filter(User.id == user_id).first()
            weight = result.weight

            # Use average if weight not entered
            if weight is None:
                if result.gender is None: weight = 180
                elif result.gender.lower() == 'male': weight = 180
                else: weight = 166
            for idx, y in enumerate(ys):
                ys[idx] = steps_to_calories(y, weight)

        return xs, ys
    
    @app.callback(Output("health-trend", "figure"),
                  [Input('health-days-dropdown', 'value'),
                   Input('health-dropdown', 'value')])
    def update_graph(days_value, trend_type):
        # Prevent request modification
        try:
            day_cnt = int(days_value)
        except:
            return "Invalid Day Selection"
    
        # Prevent larger queries
        if day_cnt < 1 or day_cnt > 365:
            return "Invalid Day Selection"
    
        try:
            xs, ys = get_recent_activity(value, day_cnt, USER_ID_TEMP,
                trend_type)
        except Exception as e:
            print e.message
            return "User Data Unavailable"
    
        return {
            'data': [{
                'x': xs,
                'y': ys
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
    
    @app.callback(Output("about-hazard", "children"),
                  [Input('hazard-dropdown', 'value'),
                   Input('map-days', 'value'),
                   Input('mile-dropdown', 'value')])
    def update_info(value, days, miles):
        # Prevent request modification
        try:
            day_cnt = int(days)
        except:
            return html.P('Invalid Day Selection')

        # Prevent larger queries
        if day_cnt < 1 or day_cnt > 365:
            return html.P('Invalid Day Selection')

        # Prevent request modification
        try:
            miles = float(miles)
        except:
            return html.P('Invalid Mile Selection')

        if miles < 0 or miles > 25:
            return html.P('Invalid Mile Selection')

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

        try:
            hazard_rate = get_vicinity_summary(USER_ID_TEMP, value, day_cnt,
                miles)
        except:
            hazard_rate = 0

        # Symbol based on hazard rate
        if hazard_rate <= 0.3:
            glyph = GOOD_GLYPH
        elif hazard_rate < 0.7:
            glyph = WARN_GLYPH
        else:
            glyph = BAD_GLYPH
        
        vicinity_msg = 'You spend {:.0%} of your time within {:.1f} miles of ' \
                        'a {} zone.'.format(hazard_rate, miles, value.lower())

        return html.Div([
            html.H4('Vicinity Summary'),
            glyph,
            html.P(
                vicinity_msg,
                style={'display': 'inline', 'padding-left': '10px'}
            ),
            html.H4('About {}'.format(value)),
            src_content,
            html.P(result.summary)
        ])
