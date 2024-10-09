import re
import random
import string


def is_valid_email(email):
    regex = r'\S+@\S+\.\S+'
    return re.fullmatch(regex, email)


def is_valid_password(password):
    # Check password length
    if len(password) < 8:
        return False

    # Check password complexity
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special_character = False

    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
        elif not char.isalnum():
            has_special_character = True

    if not (has_uppercase and has_lowercase and has_digit and has_special_character):
        return False

    return True

def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))
