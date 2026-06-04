from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.environ["MONGO_URL"]
MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]



