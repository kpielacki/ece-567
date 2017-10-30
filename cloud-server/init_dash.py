import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *


def user_dash(server):
    MAP_ACCESS_TOKEN = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMD' \
                       'AxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
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
            html.Div([dcc.Graph(id='map-graph')]),
        ], className="container")
    ], style={'padding-bottom': '20px'})

    @app.callback(Output("map-graph", "figure"))
    def update_graph():
        bearing = 0

        # df = pd.read_sql(data_query, db.engine)
        # intel_df = pd.read_sql(intel_data_query, db.engine)
        # df = create_map_labels(df, map_labels)
        # intel_df = create_map_labels(intel_df, intel_map_labels)

        # Filter for cluster.
        # if cluster_value == 'All':
        #     data_df = df
        #     intel_data_df = intel_df
        #     zoom = 3.0
        # else:
        #     data_df = df[df['Cluster'] == cluster_value]
        #     intel_data_df = intel_df[intel_df['Cluster'] == cluster_value]
        #     zoom = 12.0

        latInitial = 0
        lonInitial = 0
    
        return go.Figure(
            data=Data([
                Scattermapbox(
                    lat=[0],
                    lon=[0],
                    #text=df['map_label'].tolist(),
                    mode='markers',
                    #hoverinfo="lat+lon+text",
                    hoverinfo="lat+lon",
                    #marker=Marker(
                    #    color=site_color,
                    #    opacity=site_opacity,
                    #    size=site_marker_size,
                    #),
                ),
            ]),
            layout=Layout(
                autosize=True,
                height=500,
                margin=Margin(l=0, r=0, t=10, b=10),
                showlegend=False,
                mapbox=dict(
                    accesstoken=MAP_ACCESS_TOCKEN,
                    center=dict(
                        lat=latInitial,
                        lon=lonInitial
                    ),
                    style='dark',
                    bearing=bearing,
                    zoom=zoom
                ),
            )
        )

    return app
