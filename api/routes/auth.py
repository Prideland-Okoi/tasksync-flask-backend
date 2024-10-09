# auth.py
from api.helpers import is_valid_email, is_valid_password, generate_verification_code
from api.mail2 import send_verification_email, send_password_reset_email
from flask import Flask, request, jsonify, Blueprint
from api import db
from api import limiter
from api.models.users import User
from api.models.token import BlacklistedToken
from api import bcrypt, mail, swagger, serializer as s
from flask_jwt_extended import JWTManager, jwt_required
from datetime import datetime, timedelta
from flask_mail import Message
from werkzeug.exceptions import BadRequest
from flasgger import swag_from


auth = Blueprint('auth', __name__)

# Registration
@auth.route('/api/v1/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'Registration Details': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'},
                            'email': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input or user already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'full_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'confirm_password': {'type': 'string'}
                }
            }
        }
    ],
    'tags': ['User Authentication']
})
def registration():
    data = request.get_json()
    required_fields = ['username', 'full_name', 'email', 'password', 'confirm_password']

    # Check for missing fields
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
        return jsonify({'message': 'Password field must match confirm password field'}), 400

    # Check if the user already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    # Create a new user
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    verification_code = generate_verification_code()  # Generate verification code

    new_user = User(username=data['username'],
                    name=data['full_name'],
                    email=data['email'],
                    password_hash=password_hash,
                    verification_code=verification_code,  # Store the code
                    verification_sent_at=datetime.utcnow(), # Store the current time when the code is sent
                    verified=False)  # Not verified initially

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send verification email
    send_verification_email(data['email'], verification_code)

    new_user_data = new_user.serialize()

    response_data = {
        'message': 'User registered successfully. Please check your email to verify your account.',
        'Registration Details': new_user_data
    }
    return jsonify(response_data), 201


# Email Verification
@auth.route('/api/v1/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    code = data.get('verification_code')

    if not email or not code:
        return jsonify({'message': 'Email and verification code are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.verified:
        return jsonify({'message': 'User is already verified'}), 400

    expiration_time = timedelta(minutes=10)
    if user.verification_sent_at + expiration_time < datetime.utcnow():
        return jsonify({'message': 'Verification code has expired. Please request a new one.'}), 400

    if user.verification_code == code:
        user.verified = True
        user.verification_code = None  # Clear the code after successful verification
        user.verification_sent_at = None  # Clear the timestamp
        user.resend_attempts = 0  # Reset resend attempts
        user.last_resend_at = None  # Reset the resend timestamp
        db.session.commit()
        return jsonify({'message': 'Email verified successfully'}), 200
    else:
        return jsonify({'message': 'Invalid verification code'}), 400


# Resend verification code
@auth.route('/api/v1/resend-verification', methods=['POST'])
def resend_verification_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.verified:
        return jsonify({'message': 'User is already verified'}), 400

    # Limit the number of resends
    resend_limit = 3  # Allow 3 resend attempts
    cooldown_period = timedelta(minutes=5)  # 5-minute cooldown

    # Check if the user has exceeded the resend limit
    if user.resend_attempts >= resend_limit:
        return jsonify({'message': 'You have reached the maximum number of resend attempts. Please try again later.'}), 429

    # Check if the last resend was within the cooldown period
    if user.last_resend_at and user.last_resend_at + cooldown_period > datetime.utcnow():
        return jsonify({'message': f'Please wait {cooldown_period} before requesting another code.'}), 429

    # Generate a new verification code
    new_verification_code = generate_verification_code()

    # Update the user with the new code, resend count, and time
    user.verification_code = new_verification_code
    user.verification_sent_at = datetime.utcnow()
    user.last_resend_at = datetime.utcnow()
    user.resend_attempts += 1
    db.session.commit()

    # Send the new verification email
    send_verification_email(user.email, new_verification_code)

    return jsonify({'message': 'A new verification code has been sent to your email.'}), 200


# Login
@auth.route('/api/v1/login', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute
def login():
    data = request.get_json()
    
    # Check for missing fields
    if not data or 'email' not in data or 'password' not in data:
        raise BadRequest("Missing 'email' or 'password' in request data.")

    email = data['email']
    password = data['password']

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # Check if user exists and is verified
    if user is None:
        return jsonify({'message': 'Invalid email or password'}), 401

    if not user.verified:
        return jsonify({'message': 'Email not verified. Please verify your email before logging in.'}), 403

    # Verify the password
    if bcrypt.check_password_hash(user.password, password):  # Make sure to use the correct attribute
        access_token = create_access_token(identity=user.id)

        # Check if the token is blacklisted
        blacklisted_token = BlacklistedToken.query.filter_by(token=access_token).first()
        if blacklisted_token:
            # Token is blacklisted, remove it from blacklist
            db.session.delete(blacklisted_token)
            db.session.commit()

        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


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


@auth.route('/api/v1/forgot-password', methods=['POST'])
@limiter.limit("5 per hour", error_message="Too many reset requests. Please try again later.")
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User with this email does not exist'}), 404

    # Generate a password reset token
    token = s.dumps(email, salt='password-reset-salt')

    # Send the password reset email (implement the send_email function)
    send_password_reset_email(user.email, token)

    return jsonify({'message': 'A password reset link has been sent to your email'}), 200


@auth.route('/api/v1/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')
    
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires after 1 hour
    except Exception as e:
        return jsonify({'message': 'Invalid or expired token'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Update the user's password
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Your password has been reset successfully'}), 200

