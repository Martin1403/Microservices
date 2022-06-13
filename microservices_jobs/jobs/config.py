import os

# FOLDER SETUP
BASE = os.path.abspath(os.path.join(os.path.dirname(__name__), "jobs"))
DATABASE_FOLDER = os.path.join(BASE, "database")
os.makedirs(DATABASE_FOLDER, exist_ok=True)


class BaseConfig:
    SECRET_KEY = "somekey"
    # DATABASE CONFIG
    SQLALCHEMY_DATABASE_URI =f'sqlite:////{DATABASE_FOLDER}/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
