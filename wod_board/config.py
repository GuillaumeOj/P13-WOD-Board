import os

from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY", "foo_key_for_testing_purpose")
DATABASE_URL = os.getenv("DATABASE_URL")
