from plotly_app import app
from admin_app_config import db


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
        User.email.distinct().label('s'))
    email_options = [{'label': row.s, 'value': row.s}
                     for row in query.all()]
    
    layout = html.Div([
        html.Div([
            html.H1('Business Portal'),
            dcc.Dropdown(
                id='email-dropdown',
                options=email_options,
                value=email_options[1]['value']
            ),
            html.Div([
                html.H3('Risk Overview'),
                html.Div(['TEMP'], id='content'),
            ]),
        ], className="container")
    ], style={'padding-bottom': '20px'})
    
    @app.callback(Output("content", "children"),
                  [Input('email-dropdown', 'value')])
    def update_info(email):
        result = db.session.query(User).filter(User.email == email).first()
        if result is None:
            gender = 'N/A'
            age = 'N/A'
        else:
            gender = str(result.gender)
            age = str(result.birthday)

        return html.Div([
            html.H4(email),
            html.H4(gender),
            html.H4(age),
        ])
