import geocoder
from collections import namedtuple
from math import cos, sin, degrees, arcsin, sqrt, pow
Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

user_location = geocoder.ip('me')

#d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)]).

def calculate_distance(location1: Coordinate(int, int), location2: Coordinate(int, int)) -> int:

    body = pow((sin(location2.latitude - location1.latitude)/2), 2) + cos(location2.latitude) * cos(location1.latitude) * pow(sin((location2.longitude - location1.longitude)/2, 2))
    return int(2*6371 * arcsin(sqrt(body)))
    
