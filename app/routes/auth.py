# app/routes/auth.py
from flask import request, jsonify, session, Blueprint

# Create blueprint here
auth_bp = Blueprint('auth', __name__)

from ..models import User
from ..utils import validate_email, validate_username

# Root endpoint to see available routes
@auth_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Flask User API is running!',
        'endpoints': {
            'register': '/register (POST)',
            'login': '/login (POST)',
            'logout': '/logout (POST)',
            'profile': '/profile (GET)'
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'error': 'Username and password are required'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        email = data.get('email', '').strip() if data.get('email') else None
        
        if not validate_username(username):
            return jsonify({
                'error': 'Username must be 3-20 alphanumeric characters or underscores'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'error': 'Password must be at least 6 characters long'
            }), 400
            
        if email and not validate_email(email):
            return jsonify({
                'error': 'Invalid email format'
            }), 400
        
        existing_user = User.find_by_username(username)
        if existing_user:
            return jsonify({
                'error': 'Username already taken'
            }), 409
        
        new_user = User(username=username, password=password, email=email)
        new_user.save()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'error': 'Username and password are required'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        user = User.find_by_username(username)
        if not user or not user.check_password(password):
            return jsonify({
                'error': 'Invalid username or password'
            }), 401
        
        session['user_id'] = user.id
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user.to_dict()
    }), 200