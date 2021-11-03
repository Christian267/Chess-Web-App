from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DBHOST=os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = ':' + os.getenv('DBPASSWORD')
DBNAME = os.getenv('DBNAME')
DBPORT = os.getenv('DBPORT')

class Config:
    """Set Flask configuration vars from .env file."""
    TESTING = os.getenv('TESTING')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVERHOST', '0.0.0.0')
    SERVERPORT = os.getenv('SERVERPORT', '5000')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DBUSER}{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD=True

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True