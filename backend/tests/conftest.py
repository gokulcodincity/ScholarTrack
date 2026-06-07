import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app.config.database import SessionLocal, get_db
from app.config.settings import MONGO_DB_NAME, MONGO_URL
from app.models.user import User
from app.models.student import Student
from app.config.security import create_access_token, hash_password
from sqlalchemy import text

@pytest.fixture(scope="session")
def client():
    # Use TestClient as a context manager to trigger lifespan events (like Beanie init)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(autouse=True)
def clean_db(db):
    # Truncate tables for fresh tests (PostgreSQL only)
    db.execute(text("TRUNCATE TABLE users, students, scholarships, applications, reviewer_requests, decisions CASCADE;"))
    db.commit()


@pytest.fixture
def clean_mongodb(client):
    mongo_client = MongoClient(MONGO_URL)
    database = mongo_client[MONGO_DB_NAME]
    database["essays"].delete_many({})
    database["reviewer_notes"].delete_many({})
    try:
        yield
    finally:
        database["essays"].delete_many({})
        database["reviewer_notes"].delete_many({})
        mongo_client.close()

# Override dependency
@pytest.fixture(autouse=True)
def override_get_db(db):
    app.dependency_overrides[get_db] = lambda: db
    yield
    app.dependency_overrides = {}

@pytest.fixture
def admin_user(db):
    user = User(name="Test Admin", email="admin_test@test.com", password=hash_password("password123"), role="ADMIN", verified_email=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def admin_token(admin_user):
    return create_access_token({"id": admin_user.id, "role": "ADMIN"})

@pytest.fixture
def student_user(db):
    user = User(name="Test Student", email="student_test@test.com", password=hash_password("password123"), role="STUDENT", verified_email=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    student = Student(user_id=user.id, department="CS", cgpa=8.5, academic_year="2024-2025")
    db.add(student)
    db.commit()
    return user

@pytest.fixture
def student_token(student_user):
    return create_access_token({"id": student_user.id, "role": "STUDENT"})

@pytest.fixture
def reviewer_user(db):
    user = User(name="Test Reviewer", email="reviewer_test@test.com", password=hash_password("password123"), role="REVIEWER", verified_email=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def reviewer_token(reviewer_user):
    return create_access_token({"id": reviewer_user.id, "role": "REVIEWER"})
