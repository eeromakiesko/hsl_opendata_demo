import os
import logging
import httplib2
import json
import time
import traceback

import pandas as pd

HSL_ROUTING_API = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"

def _raw_api_call(message):
    try:
        httphandle = httplib2.Http(timeout=10)
        headers = {'Content-type': 'application/graphql'}
        body = bytes(message, 'utf-8')
        print(f"body tranposed to bytes:\n{body}")
        response, content = httphandle.request(f"{HSL_ROUTING_API}", method='POST', headers=headers, body=body)
        print(f"Config api response: {response}")
        content = json.loads(content)
    except Exception as e:
        print(f"Generic error: {traceback.format_exc()}")
        return None, None
    return response, content


def get_stop_info(stop_id=None):
    if not stop_id:
        stop_id="HSL:1173434"
    else:
        stop_id=f"HSL:{stop_id}"
    query="{stop(id: \""+stop_id+"\") {name lat lon}}"
    response, content = _raw_api_call(query)
    print(f"get_stop_info response:\n{response}\ncontent:\n{content}")
    return content

def get_trip_duration(lat1, lon1, lat2, lon2):
    query="{plan(from: {lat: "+str(lat1)+", lon: "+str(lon1)+"}, to: {lat: "+str(lat2)+", lon: "+str(lon2)+"},){itineraries{duration}}}"
    response, content = _raw_api_call(query)
    print(f"get_trip_lengt: response:\n{response}\ncontent:\n{content}")
    return content
