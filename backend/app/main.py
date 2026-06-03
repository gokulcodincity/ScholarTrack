from fastapi import FastAPI

from app.config.database import Base, engine

from app.models.user import User
from app.models.student import Student

from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScholarTrack API"
)

app.include_router(auth_router)


@app.get("/")
def home():

    return {
        "message": "ScholarTrack Backend Running"
    }