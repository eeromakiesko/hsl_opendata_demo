# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd

import hsl_api_handler

PATH_PREFIX = "/hsl_data_demo/"

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=["static/style.css"],
    requests_pathname_prefix=PATH_PREFIX,  # front-end requests prefix
    routes_pathname_prefix=PATH_PREFIX,  # backend routes prefix
    assets_folder="static"
    )


app.layout = html.Div(
    children=[
        html.H1(
            children="HSL data demo - Eero Mäki-Esko"
            ),

        html.Div(
            id='page_load',
            style={"display":"none"}
            ),

        html.Div(
            id="stop_id_header",
            children="Instert start stop ID:"
        ),

        dcc.Input(id='stop_id_start', placeholder="1173434", type='text'),

        html.Div(
            id="stop_id_header2",
            children="Instert destination stop ID:"
        ),

        dcc.Input(id='stop_id_destination', placeholder="2222234", type='text'),

        html.Div(
            id="api_response_header",
            children="API response:"
        ),
        html.Div(
            id="api_response_start"
        ),
        html.Div(
            id="api_response_destination"
        ),
        html.Div(
            id="api_response_duration"
        )
    ]
)

@app.callback(
    [
        Output('api_response_start', 'children'),
        Output('api_response_destination', 'children'),
        Output('api_response_duration', 'children'),
    ],
    [
        Input('page_load', 'children'),
        Input('stop_id_start', 'value'),
        Input('stop_id_destination', 'value')]
    )
def update_api_response(page_load, stop_id_start, stop_id_destination):
    api_response_start = hsl_api_handler.get_stop_info(stop_id_start)
    api_response_dest = hsl_api_handler.get_stop_info(stop_id_destination)

    stop_name_start = api_response_start['data']['stop']['name']
    stop_lat_start = api_response_start['data']['stop']['lat']
    stop_lon_start = api_response_start['data']['stop']['lon']

    stop_name_dest = api_response_dest['data']['stop']['name']
    stop_lat_dest = api_response_dest['data']['stop']['lat']
    stop_lon_dest = api_response_dest['data']['stop']['lon']

    api_response_duration = hsl_api_handler.get_trip_duration(
        stop_lat_start,
        stop_lon_start,
        stop_lat_dest,
        stop_lon_dest
    )

    durations = api_response_duration["data"]["plan"]["itineraries"]
    min_duration = None
    for item in durations:
        if not min_duration:
            min_duration = item["duration"]
        else:
            min_duration = min(min_duration, item["duration"])

    return [
        f"Start name:{stop_name_start}",
        f"Destination name:{stop_name_dest}",
        f"Trip minimum time (s): {min_duration}",
    ]

if __name__ == '__main__':
    # For local development
    app.run_server(debug=True, port=5000, host='0.0.0.0')
