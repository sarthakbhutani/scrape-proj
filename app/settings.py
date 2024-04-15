from os import getenv

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
ENV = getenv("ENV")

LOG_LEVEL = getenv("LOG_LEVEL")
SERVICE_NAME = getenv("SERVICE_NAME")
BASE_ROUTE = getenv("BASE_ROUTE")
FILE_HANDLING_BASE_PATH = getenv("FILE_HANDLING_BASE_PATH")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY_HOURS = int(getenv("ACCESS_TOKEN_EXPIRY_HOURS","0"))