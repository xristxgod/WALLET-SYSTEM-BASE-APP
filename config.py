import os
import logging
import decimal

decimals = decimal.Context()
decimals.prec = 18

logger = logging.getLogger(__name__)

class Config(object):
    BASE_APP_SECRET_KEY = os.getenv("BASE_APP_SECRET_KEY")
    DB_NAME = os.environ.get("POSTGRES_DB")
    USERNAME = os.environ.get("POSTGRES_USER")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")