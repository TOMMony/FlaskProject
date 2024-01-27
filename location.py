import geocoder
from collections import namedtuple
from math import cos, sin, asin, sqrt, pow, radians
from api import get_coordinate
Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

user_location = geocoder.ip('me').latlng
user_location = Coordinate(radians(user_location[0]), radians(user_location[1]))

#d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)]).

def calculate_distance(location1: Coordinate(int, int), location2: Coordinate(int, int)) -> int:
    radius = 6371
    body = pow((sin(location2.latitude - location1.latitude)/2), 2) + cos(location2.latitude) * cos(location1.latitude) * pow(sin((location2.longitude - location1.longitude)/2), 2)
    return 2* radius * asin(sqrt(body))

def user_in_radius(lecture_location) -> bool:
    distance = calculate_distance(user_location, lecture_location)
    return distance <= 1




    
