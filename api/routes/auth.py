# auth.py
from api.helpers import is_valid_email, is_valid_password
from flask import Flask, request, jsonify, Blueprint #current_app as app
from api.models.users import db, User
from api.models.token import db, BlacklistedToken
from api import bcrypt
from flask_jwt_extended import JWTManager, jwt_required
# from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)


# Method 1 - Flask JWT authentication library: https://flask-jwt-extended.readthedocs.io/


# Registration
@auth.route('/api/v1/register', methods=['POST'])
def registration():
    data = request.get_json()
    required_fields = ['username', 'email',
                       'password', 'confirm_password']

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

    # Validate password strength
    if not is_valid_password(data['password']):
        return jsonify({'message': 'Password must be at least 8 characters long and contain a combination of letters, numbers, and special characters'}), 400

    # Validate password match
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Password field must match with confirm password field'}), 400

    # Check if the user already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    # Create a new user
    password_hash = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')
    new_user = User(username=data['username'],
                    email=data['email'], password=password_hash)

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    new_user_data = new_user.serialize()

    response_data = {
        'message': 'User registered successfully',
        'Registration Details': new_user_data
    }
    return jsonify(response_data), 201


# Login
@auth.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        # Check if the token is blacklisted
        blacklisted_token = BlacklistedToken.query.filter_by(
            token=access_token).first()
        if blacklisted_token:
            # Token is blacklisted, remove it from blacklist
            db.session.delete(blacklisted_token)
            db.session.commit()
        return jsonify({'message': 'Login Success', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Logout
@auth.route('/api/v1/logout', methods=['POST'])
@jwt_required()
def logout_user():
    token = request.headers.get('Authorization')
    token_value = token.split()[1]

    # Create a new BlacklistedToken instance
    blacklisted_token = BlacklistedToken(token=token_value)

    # Add and commit the blacklisted token to the database
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({'message': 'User logged out successfully!'}), 200
