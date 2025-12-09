# app/utils.py
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password)

def verify_password(password, password_hash):
    """Verify a stored password against a provided password."""
    return check_password_hash(password_hash, password)

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric + underscore, 3-20 chars)"""
    import re
    if len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None