CREATE TABLE schedule (
  schedule_id TEXT PRIMARY KEY,
  course_name TEXT NOT NULL,
  location TEXT NOT NULL,
  time TEXT NOT NULL,
  days TEXT NOT NULL,
  id TEXT,
  FOREIGN KEY (id) REFERENCES user(id)
);