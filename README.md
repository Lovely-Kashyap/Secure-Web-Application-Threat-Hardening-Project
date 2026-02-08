# Secure-Web-Application-Threat-Hardening-Project

## Safe Sphere Overview

Safe Sphere is a secure web authentication system developed as part of a cybersecurity internship project at Cryptonic Area under the Cyber Security & Ethical Hacking Virtual Internship Program. This project was built using a single-file Flask architecture for simplicity and rapid security prototyping. The goal of this project is to demonstrate secure login and registration mechanisms while protecting the application from common web attacks.

This system focuses on threat hardening, user protection, and safe authentication practices.

## Objectives

* Build a secure login & signup system.
* Prevent unauthorized access.
* Protect against common cyber attacks.
* Demonstrate basic web security implementation.

## Security Features Implemented

### Authentication & Authorization

* User registration and login.
* Login using username OR email.
* Protected dashboard (only accessible after login).
* Logout functionality.

### Password Protection

* Passwords are hashed using bcrypt.
* No plain-text password storage.
* Strong password rules:
  * Minimum 8 characters.
  * At least 1 number.
  * At least 1 uppercase letter.

### Brute Force Protection

* Login blocked after 3 failed attempts.
* Attempt counter stored in session.

### Input Validation

* Username length validation.
* Email format validation.
* Password strength enforcement.
* Duplicate email prevention.

### Session Security

* Session-based login tracking.
* Unauthorized users redirected to login page.

## Screenshots

Screenshots of the following have been included in the `/screenshots` folder:

* Signup page
* Login page
* Dashboard after login
* Empty field validation
* Invalid login attempt
* SQL injection attempt blocked
* Password validation error
* Duplicate email detection
* Brute force protection

## Tech Stack

1. Python
2. Flask
3. SQLite
4. Bcrypt
5. HTML/CSS (via Flask templates)

## Project Structure

Since the entire application is in one file:

```
safe-sphere-secure-app/
│
├── app.py            # Complete application (Backend + Frontend + Security)
├── users.db          # Auto-created SQLite database
├── requirements.txt
└── README.md
```

## Installation & Setup

1️⃣ Install Dependencies
```
pip install -r requirements.txt
```

2️⃣ Run the Application
```
python app.py
```

3️⃣ Open in Browser
```
http://127.0.0.1:5000
```

## Learning Outcomes

Through this project, I learned:

* Basics of secure web development
* Authentication and session handling
* Protection against SQL Injection
* Brute force attack prevention
* Input validation techniques

## Author

**Lovely Kashyap**
Cyber Security & Ethical Hacking Intern - Cryptonic Area
