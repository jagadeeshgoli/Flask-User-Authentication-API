# tests/test_auth.py
import unittest
import json
from app import create_app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test app and client"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test"""
        self.app_context.pop()

    def test_register_success(self):
        """Test successful user registration"""
        response = self.client.post('/register', 
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'password': 'password123',
                                      'email': 'test@example.com'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'testuser')

    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post('/register', 
                                  data=json.dumps({
                                      'username': 'testuser'
                                      # Missing password
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_register_duplicate_username(self):
        """Test registration with duplicate username"""
        # First registration
        self.client.post('/register', 
                        data=json.dumps({
                            'username': 'testuser',
                            'password': 'password123'
                        }),
                        content_type='application/json')
        
        # Second registration with same username
        response = self.client.post('/register', 
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'password': 'password456'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('already taken', data['error'])

    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        response = self.client.post('/register', 
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'password': 'password123',
                                      'email': 'invalid-email'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_login_success(self):
        """Test successful login"""
        # Register first
        self.client.post('/register', 
                        data=json.dumps({
                            'username': 'loginuser',
                            'password': 'password123'
                        }),
                        content_type='application/json')
        
        # Login
        response = self.client.post('/login', 
                                  data=json.dumps({
                                      'username': 'loginuser',
                                      'password': 'password123'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertIn('user', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/login', 
                                  data=json.dumps({
                                      'username': 'nonexistent',
                                      'password': 'wrongpassword'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post('/login', 
                                  data=json.dumps({
                                      'username': 'testuser'
                                      # Missing password
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_profile_requires_auth(self):
        """Test that profile endpoint requires authentication"""
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Not authenticated', data['error'])

    def test_logout(self):
        """Test logout functionality"""
        # Register and login
        self.client.post('/register', 
                        data=json.dumps({
                            'username': 'logoutuser',
                            'password': 'password123'
                        }),
                        content_type='application/json')
        
        login_response = self.client.post('/login', 
                                        data=json.dumps({
                                            'username': 'logoutuser',
                                            'password': 'password123'
                                        }),
                                        content_type='application/json')
        
        self.assertEqual(login_response.status_code, 200)
        
        # Logout
        logout_response = self.client.post('/logout')
        self.assertEqual(logout_response.status_code, 200)
        
        # Try to access profile after logout
        profile_response = self.client.get('/profile')
        self.assertEqual(profile_response.status_code, 401)

    def test_register_short_password(self):
        """Test registration with too short password"""
        response = self.client.post('/register', 
                                  data=json.dumps({
                                      'username': 'shortpassuser',
                                      'password': '123'  # Too short
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('6 characters', data['error'])

if __name__ == '__main__':
    unittest.main()