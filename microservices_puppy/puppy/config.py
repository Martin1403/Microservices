import os

base = os.path.abspath(os.path.dirname(__file__))
database = os.path.join(base, "database")
os.makedirs(database, exist_ok=True)


class BaseConfig:
    API_TITLE = 'Puppy Rest Api'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_JSON_PATH = 'openapi.json'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'  # noqa: E501
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    SECRET_KEY = "somekey"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(database, 'data.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(BaseConfig):
    debug = False


class Development(BaseConfig):
    debug = True
