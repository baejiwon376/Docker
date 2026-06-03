from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "courses.json")


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def load_courses():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return {"message": "FastAPI Course Records Server"}


@app.get("/courses")
def get_courses():
    return load_courses()


@app.post("/courses")
def add_course(course: Course):
    data = load_courses()

    new_course = {
        "course_name": course.course_name,
        "year": course.year,
        "semester": course.semester,
        "grade": course.grade,
    }

    data.append(new_course)
    save_courses(data)

    return {
        "message": "Course added successfully",
        "added_course": new_course,
    }
