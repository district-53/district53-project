import os
from dotenv import load_dotenv

VM_ENV_FILE = os.environ["HALL_ENV_FILE", "/etc/hall/app.env"]
if os.path.isfile(VM_ENV_FILE) and os.access(VM_ENV_FILE, os.R_OK):
    load_dotenv(VM_ENV_FILE)
load_dotenv()

class Config:
    EXILE_SWITCH = os.environ["EXILE_SWITCH", "0"] == "1"
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"] 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_ENDPOINT = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
    S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
    S3_BUCKET = os.environ["S3_BUCKET", "avatars"]

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 