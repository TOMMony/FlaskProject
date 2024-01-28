from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, points):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.points = points

    @staticmethod
    def add_point(user_id):
        db = get_db()
        curr_points = User.get_points(user_id)
        db.execute(
            "UPDATE user SET points = ? WHERE id = ?", (curr_points + 1, user_id)
        )
        db.commit()

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], points=user[4]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, points):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic, points) "
            "VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic, points),
        )
        db.commit()

    @staticmethod
    def get_points(user_id):
        db = get_db()
        try:
            points = db.execute(
                "SELECT points FROM user WHERE id = ?", (user_id,)
            ).fetchone()
        except:
            #User has not been created yet
            print("User has not been created yet")
            return 0
        
        return points[0]