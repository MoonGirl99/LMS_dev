# test_main.py

import pytest
from fastapi.testclient import TestClient

from main import SessionLocal, app, create_tables, create_engine, db

# Create test database
DATABASE_URL = "postgresql://test_lms:admin@test_postgres:5432/test_lmsdb"
app.dependency_overrides[create_tables] = lambda: None

app.dependency_overrides[db] = lambda: SessionLocal(bind=create_engine(DATABASE_URL))

client = TestClient(app)


@pytest.fixture(scope="module")
def test_app():
    create_tables()
    return app


def test_create_course(test_app):
    response = client.post(
        "/courses/",
        json={"name": "Test Course", "description": "Test Description", "user_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Course"


def test_read_course(test_app):
    # Assuming there is a course with ID 1 in the database
    response = client.get("/courses/1")
    assert response.status_code == 200
    assert response.json()["course_id"] == 1


def test_create_lesson(test_app):
    # Assuming there is a course with ID 1 in the database
    response = client.post(
        "/courses/1/lessons/",
        json={"title": "Test Lesson", "content": "Test Content"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Lesson"


def test_read_lesson(test_app):
    # Assuming there is a lesson with ID 1 in the database
    response = client.get("/lessons/1")
    assert response.status_code == 200
    assert response.json()["lesson_id"] == 1


def test_create_user_profile(test_app):
    response = client.post(
        "/user_profiles/", json={"username": "test_user", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


def test_read_user_profile(test_app):
    # Assuming there is a user profile with ID 1 in the database
    response = client.get("/user_profiles/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

