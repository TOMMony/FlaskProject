import urllib.request
import urllib.parse
import json

URL_COURSES = 'https://api.peterportal.org/rest/v0/courses/'

def get_33():
    request = urllib.request.Request(f'{URL_COURSES}I&CSCI33')
    response = json.loads(urllib.request.urlopen(request).read().decode(encoding='utf-8'))
    return response
