# init.py
from flask import Flask
from api.models import db
from api.config import Config
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Create Flask app instance
app = Flask(__name__)

# Create instances of Flask extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate()


def create_app():
    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Create the database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    from api.routes import auth
    app.register_blueprint(auth)
    app.register_blueprint(users)

    return app
