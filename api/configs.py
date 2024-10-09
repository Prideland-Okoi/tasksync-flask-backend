import os
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

load_dotenv()



# class postgresql_Config:
# Configure the database connection using the environment variables
    # SQLALCHEMY_DATABASE_URI = (
    # f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    # f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # New for JWT


class Config:
    # Set app secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'JJHGGKSFJDJSJKmkfkdhhg'
    DEBUG = False

    # Set database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tasksync.db'

    # Disable modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set JWT token expiration time
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


    # Email configuration for Flask-Mail loaded from environment variables
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') == 'True'
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

# Create a function to initialize the serializer with the current app config
def create_serializer(app):
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])

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
