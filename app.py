from flask import Flask, render_template, request, redirect, url_for
from flask_login import (LoginManager,
                         current_user,
                         login_required,
                         login_user,
                         logout_user,)
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from user import User
from schedule import Schedule
import json 
import sqlite3
import os

# Configuration DELTE BEFORE POST
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)



# These routes render Jinja templates. If you don't
# want to make a separate frontend, you can use Flask
# templates to create a website!
# Read more here: https://flask.palletsprojects.com/en/2.0.x/quickstart/#rendering-templates


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/")
def index():
    if current_user.is_authenticated:
        '''return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )'''
        current_user.points = 10
        print(current_user.points)
        print('points changed')
        return redirect("main_page")
    else:
        return '<a class="button" href="/login">Google Login</a>'
    
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, points=User.get_points(unique_id)
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture, 0)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/main_page")
@login_required
def main_page():
    return render_template("index.html", points = current_user.points)

@app.route("/process_points")
def render_points():
    print("User id:", current_user.id)
    print("Points before adding:", User.get_points(current_user.id))
    User.add_point(current_user.id)
    user_points = User.get_points(current_user.id)
    print("Points after adding:", user_points)

    return render_template('points.html', points = user_points)

@app.route("/schedule")
@login_required
def schedule():
    print(f"lol {_get_scheduled_courses(current_user.id)}")
    return render_template("table.html", scheduled_courses = _get_scheduled_courses(current_user.id))

@app.route("/handle_data", methods=["POST"])
@login_required
def handle_data():
    schedule_id = Schedule.create_id()
    course_name = request.form["coursename"]
    location = request.form["location"]
    time = request.form["time"]
    days = ''
    if "monday" in request.form:
        days += "M"
    if "tuesday" in request.form:
        days += "T"
    if "wednesday" in request.form:
        days += "W"
    if "thursday" in request.form:
        days += "Th"
    if "friday" in request.form:
        days += "F"
    schedule = Schedule(schedule_id, course_name, location, time, days, current_user.id)
    if not Schedule.get(schedule_id):
        Schedule.create(schedule_id, course_name, location, time, days, current_user.id)
    return redirect(url_for("schedule"))

def _get_scheduled_courses(current_user_id) -> list:
    with sqlite3.connect("sqlite_db") as db:
        cursor = db.cursor()
        sql = f"SELECT * FROM schedule WHERE id = '{current_user_id}'"
        cursor.execute(sql)
        return cursor.fetchall()




if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")
