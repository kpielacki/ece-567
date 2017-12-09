from plotly_app import app
from admin_app_config import db
from utils import (vicinity_rate, GOOD_GLYPH, WARN_GLYPH, BAD_GLYPH,
                   bmi_to_glyph)

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

    query = db.session.query(
        User.id.distinct().label('s'))
    uid_options = [{'label': str(row.s), 'value': str(row.s)}
                     for row in query.all()]
    
    layout = html.Div([
        html.Div([
            html.H1('Business Portal'),
            dcc.Dropdown(
                id='uid-dropdown',
                options=uid_options,
                value='1',
            ),
            html.Div([
                html.H3('Risk Overview'),
                html.Div(['Loading...'], id='content'),
            ]),
        ], className="container")
    ], style={'padding-bottom': '20px'})

    def get_profile(uid):
        result = db.session.query(User).filter(User.id == uid).first()
        email = 'N/A'
        gender = 'N/A'
        age = 'N/A'
        height = 'N/A'
        weight = 'N/A'
        bmi = html.P('N/A')
        if result is not None:
            email = str(result.email).capitalize()
            gender = str(result.gender).capitalize()
            height = '{:.0f}'.format(result.height)
            weight = '{:.0f}'.format(result.weight)
            bmi = bmi_to_glyph(result.BMI())
            if result.birthday is None:
                age = 'N/A'
            else:
                age = (datetime.date.today() - result.birthday).days / 365
                if age <= 1:
                    age = (datetime.date.today() - result.birthday).days
                    age = str(age) + ' Days'
                else:
                    age = str(age) + ' Years'
        return email, age, gender, height, weight, bmi

    def get_activity(uid):
        date_from = datetime.date.today() - datetime.timedelta(days=365)
        result = db.session.query(UserSteps) \
            .filter(UserSteps.user_id == uid) \
            .filter(UserSteps.date >= date_from) \
            .order_by(UserSteps.date.desc()).all()
        xs = []
        ys = []
        for r in result:
            xs.append(r.date)
            ys.append(r.step_count)

        {
            'data': [{
                'x': xs,
                'y': ys
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }

        return dcc.Graph(
            id='health-trend',
            figure={
                'data': [{
                'x': xs,
                'y': ys
                }],
                'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
            },
            style={'max-height': '300px'}
        )

    def get_hazard_summary(uid):
        date_from = datetime.date.today() - datetime.timedelta(days=365)
        hazards = db.session.query(HazardSummary) \
                  .order_by(HazardSummary.hazard_category.asc()).all()

        summary = []
        for hazard in hazards:
            miles = hazard.bad_distance
            if miles is None: miles = 0.1
            category = hazard.hazard_category

            # Get hazard points
            results = db.session.query(HazardLocation) \
                .filter(HazardLocation.hazard_category == category).all()
            hazard_points = [(r.latitude, r.longitude) for r in results]

            # Get user points
            results = db.session.query(UserLocation) \
                .filter(UserLocation.user_id == uid) \
                .filter(UserLocation.date >= date_from).all()
            user_points = [(r.latitude, r.longitude) for r in results]
            rate = vicinity_rate(hazard_points, user_points, miles)
            vicinity_msg = 'The user has spent {:.0%} of their time within ' \
                           'the not recommended distance of {:.1f} miles ' \
                           'near a {} zone.'.format(rate, miles,
                                                    category.lower())
            if rate <= 0.3: glyph = GOOD_GLYPH
            elif rate < 0.7: glyph = WARN_GLYPH
            else: glyph = BAD_GLYPH
            summary.append(html.Div([
                glyph,
                html.P(
                    vicinity_msg,
                    style={'display': 'inline', 'padding-left': '10px'}
                )
            ]))
        return html.Div(summary)
    
    @app.callback(Output("content", "children"),
                  [Input('uid-dropdown', 'value')])
    def update_info(uid):
        try:
            email, age, gender, height, weight, bmi = get_profile(uid)
        except:
            email = 'N/A'
            age = 'N/A'
            gender = 'N/A'
            height = 'N/A'
            weight = 'N/A'
            bmi = html.P('N/A')

        try:
            overview = get_hazard_summary(uid)
        except:
            overview = html.P('Overview Not Available')

        try:
            activity_trend = get_activity(uid)
        except:
            activity_trend = html.P('Activity Not Available')

        return html.Div([
            html.Div([
                html.H4('Profile'),
                html.Ul([
                    html.Li('Email: {}'.format(email)),
                    html.Li('Gender: {}'.format(gender)),
                    html.Li('Age: {}'.format(age)),
                    html.Li('Height (inches): {}'.format(height)),
                    html.Li('Weight (lbs): {}'.format(weight)),
                    html.Li(bmi)
                ]),
            ]),
            html.Div([
                html.H4('Overview'),
                overview
            ]),
            html.Div([
                html.H4('Year Step Activity'),
                activity_trend
            ]),
        ])
