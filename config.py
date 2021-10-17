from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Set Flask configuration vars from .env file."""
    TESTING = os.getenv('TESTING')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
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