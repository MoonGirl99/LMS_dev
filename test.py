from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, db, create_tables



DATABASE_URL_TEST = "postgresql://lms:admin@postgres:5432/lmsdb"
engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

app.dependency_overrides[db] = TestingSessionLocal

client = TestClient(app)


def setup_function():
    create_tables()


def test_create_course():
    response = client.post("/courses/", json={"name": "Test Course", "description": "Test Description", "user_id": 1})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Course"
    assert response.json()["description"] == "Test Description"
    assert response.json()["user_id"] == 1


def test_read_course():
    response = client.get("/courses/1")
    assert response.status_code == 200
    assert response.json()["course_id"] == 1


def test_create_lesson():
    response = client.post("/courses/1/lessons/", json={"title": "Test Lesson", "content": "Test Content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Lesson"
    assert response.json()["content"] == "Test Content"
    assert response.json()["course_id"] == 1


def test_read_lesson():
    response = client.get("/lessons/1")
    assert response.status_code == 200
    assert response.json()["lesson_id"] == 1


def test_create_user_profile():
    response = client.post("/user_profiles/", json={"username": "TestUser", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "TestUser"
    assert response.json()["email"] == "test@example.com"


def test_read_user_profile():
    response = client.get("/user_profiles/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
