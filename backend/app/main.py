from fastapi import FastAPI

from app.config.database import engine
from app.models.base import Base

from app.routes.user_routes import router as user_router
from app.routes.student_routes import router as student_router
from app.models.user import User
from app.models.student import Student

from app.models.scholarship import Scholarship
from app.models.application import Application
from app.models.decision import Decision

from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.student_routes import router as student_router

from app.routes.scholarship_routes import (
    router as scholarship_router
)

from app.routes.application_routes import (
    router as application_router
)

from app.routes.admin_routes import (
    router as admin_router
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScholarTrack API",
    version="1.0.0"
)

# Authentication Routes
app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(student_router)

# Users
app.include_router(user_router)

# Students
app.include_router(student_router)

# Scholarship Routes
app.include_router(scholarship_router)

# Application Routes
app.include_router(application_router)

# Admin Routes
app.include_router(admin_router)


@app.get("/")
def home():

    return {
        "message": "ScholarTrack Backend Running"
    }