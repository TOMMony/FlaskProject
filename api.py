import urllib.request
import urllib.parse
import json
from collections import namedtuple
from math import radians

FORWARD_SEARCH_URL = 'https://nominatim.openstreetmap.org/search?format=json&q='

Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

def get_coordinate(named_location: str) -> Coordinate:
    named_location += ''
    encoded_location = urllib.parse.quote(named_location)
    request = urllib.request.Request(FORWARD_SEARCH_URL + encoded_location)
    response = urllib.request.urlopen(request)
    data = json.load(response)[0]
    return Coordinate(radians(float(data['lat'])), radians(float(data['lon'])))



