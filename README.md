# Flask User Authentication API

A secure REST API built by **Goli Jagadeesh** for user registration, login, logout, and protected profile access using session-based authentication. Designed as a lightweight backend to understand core API concepts, password hashing, and authentication workflows.

##  Developer
**Goli Jagadeesh**  
Python & Backend Developer (Fresher)  
 Lam, Guntur, Andhra Pradesh — 522034  
 7671086404  
 jagadeeshgoli22@gmail.com  
 GitHub: https://github.com/jagadeeshgoli  
 LinkedIn: https://linkedin.com/in/jagadeeshgoli

---

##  Features
-  Secure user registration with validation  
-  Password hashing using Werkzeug  
-  Session-based login & logout  
-  Protected `/profile` endpoint  
-  Clean JSON responses  
-  Built-in error handling  

---

## Tech Stack
| Component | Technology |
|----------|------------|
| Language | Python 3.8+ |
| Framework | Flask |
| Security | Werkzeug Password Hashing |
| Storage | In-memory dictionary (`users_db`) |
| Auth System | Flask Sessions |

---

##  API Endpoints

### **1 POST /register**
Register a new user  
Validates username, email, and password.

### **2 POST /login**
Authenticates user and creates session.

### **3 GET /profile**
Returns user details.  
 Requires login (protected route)

### **4 POST /logout**
Destroys user session.

### **5 GET /**
Returns API status + available routes.

---

##  Installation

### Requirements
```bash
pip install Flask

````

### Setup

```bash
git clone <your-repository-url>
cd flask-auth-api

python -m venv venv
source venv/bin/activate          # Windows → venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

Flask will start at:

```
http://127.0.0.1:5000
```

---

##  Usage Examples

### **Register User**

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "jai", "password": "password123", "email": "jai@example.com"}'
```

### **Login**

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jai", "password": "password123"}' \
  -c cookies.txt
```

### **Access Profile**

```bash
curl -X GET http://127.0.0.1:5000/profile \
  -b cookies.txt
```

### **Logout**

```bash
curl -X POST http://127.0.0.1:5000/logout \
  -b cookies.txt
```

---

##  Error Codes

| Status | Meaning                      |
| ------ | ---------------------------- |
| `400`  | Validation failed            |
| `401`  | Unauthorized / Not logged in |
| `409`  | Username already exists      |
| `500`  | Internal server error        |

---

##  Security Features

* Password hashing (Werkzeug)
* Secure session cookies
* Validation for all inputs
* No plain-text password storage
* Protected API endpoints

---

##  Testing

Run unit tests:

```bash
python -m pytest tests/ -v
```

---

##  Future Enhancements

* PostgreSQL / MySQL database integration
* JWT-based authentication
* Forgot password + email OTP
* Rate limiting
* Admin dashboard

---

##  License

MIT License — free for personal & commercial use.

---

##  Support

For issues or collaboration:
** [jagadeeshgoli22@gmail.com](mailto:jagadeeshgoli22@gmail.com)**
