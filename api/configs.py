import os
from datetime import timedelta

class Config:
    # # Set app secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'JJHGGKSFJDJSJKmkfkdhhg'
    DEBUG = False

    # # Set database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tasksync.db'

    # Disable modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set JWT token expiration time
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) 

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config():
    environment = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(environment, DevelopmentConfig)