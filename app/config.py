import os

postgresql = os.environ.get("DDTYPE")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
postgresserver = os.environ.get("SERVER")
db = os.environ.get("DBNAME")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")