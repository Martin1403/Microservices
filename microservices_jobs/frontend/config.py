import os
import secrets


class BaseConfig:
    SECRET_KEY = "mysecretkey"
    WTF_CSRF_TOKEN = "mysecretkey"
    BASE = os.path.abspath(os.path.dirname(__file__))