"""Mapping APIs for Flask Cafe"""

import requests
import os

from secret import MAPQUEST_API_KEY as API_KEY


def get_map_url(address, city, state):
    """Get MapQuest URL for a static map for this location"""

    base = f"https://www.mapquestapi.com/staticmap/v5/map?key={API_KEY}"
    where = f"{address},{city},{state}"
    return f"{base}&center={where}&size=@2x&zoom=15&locations={where}"


def save_map(id, address, city, state):
    """Get static map and save in static/maps directory of this app"""

    url = get_map_url(address, city, state)
    response = requests.get(url)

    path = os.path.abspath(os.path.dirname(__file__))

    with open(f"{path}/static/maps/{id}.jpg", "wb") as file:
        file.write(response.content)