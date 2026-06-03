from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


@app.get("/")
def root():
    return {"message": "FastAPI Course Records Server"}


@app.get("data/courses.json")
def get_courses():
    with open("courses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@app.post("/courses")
def add_course(course: Course):
    with open("courses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append({
        "course_name": course.course_name,
        "year": course.year,
        "semester": course.semester,
        "grade": course.grade
    })

    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "message": "Course added successfully",
        "added_course": {
            "course_name": course.course_name,
            "year": course.year,
            "semester": course.semester,
            "grade": course.grade
        }
    }