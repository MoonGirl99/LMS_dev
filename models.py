# Packages
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship


# Database

# SQLAlchemy models
Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)

    lessons = relationship("Lesson", back_populates="course")
    users = relationship("UserCourse", back_populates="course")


class Lesson(Base):
    __tablename__ = "lessons"
    lesson_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    course_id = Column(Integer, ForeignKey("courses.course_id", onupdate="CASCADE", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)

    course = relationship("Course", back_populates="lessons")
    users = relationship("UserLesson", back_populates="lesson")


class UserProfile(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String, index=True)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)

    courses = relationship("UserCourse", back_populates="user")
    lessons = relationship("UserLesson", back_populates="user")

    def set_password(self, password):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.hashed_password)


class UserCourse(Base):
    __tablename__ = "user_courses"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True)

    user = relationship("UserProfile", back_populates="courses")
    course = relationship("Course", back_populates="users")


class UserLesson(Base):
    __tablename__ = "user_lessons"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id", ondelete="CASCADE"), primary_key=True)
    completed_at = Column(TIMESTAMP)

    user = relationship("UserProfile", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="users")
