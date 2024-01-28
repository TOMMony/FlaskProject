from db import get_db

class Schedule:
    _id = 0
    
    def __init__(self, schedule_id, course_name, location, time, days, id):
        self.shcedule_id = schedule_id
        self.course_name = course_name
        self.location = location
        self.time = time
        self.days = days
        self.id = id

    @staticmethod
    def create_id():
        db = get_db()
        max_id = db.execute(
            "SELECT MAX(schedule_id) FROM schedule"
        ).fetchone()[0]
        print(max_id)
        if not max_id:
            return 0
        return int(max_id) + 1

    @staticmethod
    def get(schedule_id):
        db = get_db()
        schedule = db.execute(
            "SELECT * FROM schedule WHERE schedule_id = ?", (schedule_id,)
        ).fetchone()
        if not schedule:
            return None
        schedule = Schedule(
            schedule_id=schedule[0], course_name=schedule[1], location=schedule[2], time=schedule[3], days=schedule[4], id=schedule[5]
        )
        return schedule

    @staticmethod
    def create(schedule_id, course_name, location, time, days, id):
        db = get_db()
        db.execute(
            "INSERT INTO schedule (schedule_id, course_name, location, time, days, id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (schedule_id, course_name, location, time, days, id),
        )
        db.commit()

    @staticmethod
    def delete(course_name, id):
        db = get_db()
        db.execute(
            "DELETE FROM schedule WHERE course_name = ? AND id = ?",
            (course_name, id),
        )
        db.commit()
