# Imports
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_limiter import FastAPILimiter, Depends as LimiterDepends
from fastapi_limiter.depends import RateLimiter
from loguru import logger

from models import Course, Lesson, UserProfile, Base




# Database
DATABASE_URL = "postgresql://lms:admin@postgres:5432/lmsdb"
engine = create_engine(DATABASE_URL)

# FastAPI
app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Logging
logger.add("logs/application.log", rotation="500 MB", level="INFO")

# Rate Limit
FastAPILimiter.init()
rate_limit = RateLimiter(10, 1)

# Defined Variables
courses = []
lessons = []
user_profiles = []


# Routes
@app.post("/courses/")
def create_course(name: str, description: str, user_id: int):
    course = db.Course(name=name, description=description, user_id=user_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    db.close()
    return course


@app.get("/courses/{course_id}")
def read_course(course_id: int):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    db.close()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# Lessons
@app.post("/courses/{course_id}/lessons/")
def create_lesson(course_id: int, title: str, content: str):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
        db.close()
        raise HTTPException(status_code=404, detail="Course not found")

    lesson = Lesson(title=title, content=content, course_id=course_id)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    db.close()
    return lesson


@app.get("/lessons/{lesson_id}")
def read_lesson(lesson_id: int):
    lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
    db.close()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# User profile
@app.post("/user_profiles/")
def create_user_profile(username: str, email: str):
    user_profile = UserProfile(username=username, email=email)
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    db.close()
    return user_profile


@app.get("/user_profiles/{user_id}")
def read_user_profile(user_id: int):
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    db.close()
    if user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user_profile


# create tables
def create_tables():
    Base.metadata.create_all(bind=engine)




