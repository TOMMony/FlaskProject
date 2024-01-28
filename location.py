import geocoder
import datetime
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

def get_current_course(courses) -> tuple|None:
    current_day = datetime.datetime.today().weekday()
    current_time = datetime.datetime.now().time().hour * 60 + datetime.datetime.now().time().minute
    for course in courses:
        start_time = int(course[3][:-2]) * 60 + int(course[3][-2:])
        end_time = start_time + 50

        days = course[4]
        if current_day == 0 and "M" not in days:
            continue
        elif current_day == 1 and "Tu" not in days:
            continue
        elif current_day == 2 and "W" not in days:
            continue
        elif current_day == 3 and "Th" not in days:
            continue
        elif current_day == 4 and "F" not in days:
            continue
        elif current_day == 5 and "Sa" not in days:
            continue
        elif current_day == 6 and "Su" not in days:
            continue
        if start_time <= current_time <= end_time:
            return course
    return None




    
