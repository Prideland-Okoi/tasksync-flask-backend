# routes/__init__.py
from api.routes.auth import auth
from flask import Blueprint

# Create blueprints for each route module
auth = Blueprint('auth', __name__)
# users = Blueprint('users', __name__)
