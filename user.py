from flask_login import UserMixin
from db import get_db
import pyrebase

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, points):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.points = points
    
    @staticmethod
    def add_point(user_id):
        #db = get_db()
        #curr_points = User.get_points(user_id)
        #db.execute(
        #    "UPDATE user SET points = ? WHERE id = ?", (curr_points + 1, user_id)
        #)
        #db.commit()
        currentpoints = int(__class__.get_points(user_id))
        new = currentpoints + 1
        __class__.updatepoints(user_id, str(new))

    @staticmethod
    def get(user_id):
        #db = get_db()
        #user = db.execute(
        #    "SELECT * FROM user WHERE id = ?", (user_id,)
        #).fetchone()
        #if not user:
        #    return None
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()
        user = firebase_db.child('users').child(user_id).get()
        if (user.val() is None):
            return None
        
        user = User(
            id_=user_id, name=user[1].val(), email=user[0].val(), profile_pic=user[3].val(), points=user[2].val()
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, points):
        #db = get_db()
        #db.execute(
        #    "INSERT INTO user (id, name, email, profile_pic, points) "
        #    "VALUES (?, ?, ?, ?, ?)",
        #    (id_, name, email, profile_pic, points),
        #)
        #db.commit()
        __class__.registerAccount(id_, name, email, profile_pic, points)

    @staticmethod
    def get_points(user_id):
        #db = get_db()
        #try:
        #    points = db.execute(
        #        "SELECT points FROM user WHERE id = ?", (user_id,)
        #    ).fetchone()
        #except:
        #    #User has not been created yet
        #    print("User has not been created yet")
        #    return 0
        return __class__.getPoints(user_id)
        #return points[0]
    
    ###firebase methods###
    @staticmethod
    def registerAccount(id: str, name: str, email: str, pic: str, points=0) -> None:
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()

        data = {"name": name, "points": str(points), "email": email, "profile_pic": pic}
        firebase_db.child("users").child(id).set(data)

    @staticmethod
    def updatepoints(id: str, points) -> None:
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()

        firebase_db.child("users").child(id).update({"points": str(points)})
    
    @staticmethod
    def getName(id: str):
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()

        try:
            info = firebase_db.child('users').child(id).get()
            return info[1].val()
        except TypeError:
            pass

    @staticmethod
    def getPoints(id: str):
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()
        try:
            info = firebase_db.child('users').child(id).get()
            return info[2].val()
        except TypeError:
            pass
    
    @staticmethod
    def getEmail(id: str):
        firebaseConfig = {
            "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
            "authDomain": "zotz-ce6bb.firebaseapp.com",
            "projectId": "zotz-ce6bb",
            "storageBucket": "zotz-ce6bb.appspot.com",
            "messagingSenderId": "693632128029",
            "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
            "measurementId": "G-DLMPNFSZKV",
            "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        firebase_db = firebase.database()

        try:
            info = firebase_db.child('users').child(id).get()
            return info[0].val()
        except TypeError:
            pass
    ###end of firebase methods###
#User.registerAccount("testid", "testname", "testemail", "testpic", "testpoints")
#User.updatepoints("testid", "updatetest")
firebaseConfig = {
    "apiKey": "AIzaSyChypQQX7SCGsgTdYcag1_6vBilrUEXP6o",
    "authDomain": "zotz-ce6bb.firebaseapp.com",
    "projectId": "zotz-ce6bb",
    "storageBucket": "zotz-ce6bb.appspot.com",
    "messagingSenderId": "693632128029",
    "appId": "1:693632128029:web:4e780d058c5bc2b33d22f4",
    "measurementId": "G-DLMPNFSZKV",
    "databaseURL": "https://zotz-ce6bb-default-rtdb.firebaseio.com/"
    }

#firebase = pyrebase.initialize_app(firebaseConfig)
#firebase_db = firebase.database()
#person = firebase_db.child('users').child('whatteuhf').get()
#print(person.val() is None)

