# app/models.py
import uuid
from datetime import datetime
from .utils import hash_password, verify_password

# In-memory user storage (replace with DB later)
users_db = {}

class User:
    def __init__(self, username, password, email=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = hash_password(password)
        self.created_at = datetime.now()
    
    def check_password(self, password):
        return verify_password(password, self.password_hash)
    
    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
        if include_password:
            data['password_hash'] = self.password_hash
        return data

    @staticmethod
    def find_by_username(username):
        for user_data in users_db.values():
            if user_data.username == username:
                return user_data
        return None
    
    @staticmethod
    def find_by_id(user_id):
        return users_db.get(user_id)

    def save(self):
        users_db[self.id] = self
        return self