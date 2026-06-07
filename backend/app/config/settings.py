from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL, make_url

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_MAINTENANCE_DB = os.getenv("POSTGRES_MAINTENANCE_DB", "postgres")


def _build_database_url():
    if all([
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_USER,
        POSTGRES_PASSWORD is not None,
        POSTGRES_DB,
    ]):
        return URL.create(
            "postgresql+psycopg2",
            username=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=int(POSTGRES_PORT),
            database=POSTGRES_DB,
        ).render_as_string(hide_password=False)

    return os.environ["DATABASE_URL"]


DATABASE_URL = _build_database_url()
_DATABASE_SETTINGS = make_url(DATABASE_URL)

POSTGRES_HOST = POSTGRES_HOST or _DATABASE_SETTINGS.host
POSTGRES_PORT = POSTGRES_PORT or str(_DATABASE_SETTINGS.port or 5432)
POSTGRES_USER = POSTGRES_USER or _DATABASE_SETTINGS.username
POSTGRES_PASSWORD = (
    POSTGRES_PASSWORD
    if POSTGRES_PASSWORD is not None
    else _DATABASE_SETTINGS.password
)
POSTGRES_DB = POSTGRES_DB or _DATABASE_SETTINGS.database


MONGO_URL = os.environ["MONGO_URL"]
MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]
