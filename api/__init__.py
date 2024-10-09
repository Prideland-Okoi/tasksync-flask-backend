# init.py
from flask import Flask
# from api.models import db
from flask_sqlalchemy import SQLAlchemy
# from api.configs import Config
from api.configs import get_config, create_serializer
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger

# Global serializer (will be initialized in create_app)
serializer = None

# Create Flask app instance
app = Flask(__name__)

# Initialize Limiter
limiter = Limiter(
    get_remote_address,  # Use the client's IP address for limiting
    default_limits=["5 per hour"],  # Default limit of 5 requests per hour for all routes
    # storage_uri='redis:'
)

# Create instances of Flask extensions
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate()
swagger = Swagger()

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    # Create and configure the Flask app
    # Load configuration from the Config class
    global serializer
    config = get_config()
    app.config.from_object(config)
    # app.config.from_object(get_config())

    mail.init_app(app)

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask extensions
    mail.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)

    # Attach the limiter to the app
    limiter.init_app(app)

    # Initialize the serializer with the app's config
    serializer = create_serializer(app)


    # Create the database tables (if they don't exist)
    # with app.app_context():
    #     db.create_all()

    from api.routes.auth import auth
    # from api.routes.users import users
    app.register_blueprint(auth)
    # app.register_blueprint(users)

    return app
