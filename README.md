# 🎓 Student Management System (SMS)

A secure, CRUD-based web application built with Flask, SQLAlchemy, Flask-WTF, and Bootstrap 5. This app allows admins to manage student records in a clean and responsive UI.

---

## ✨ Features

- 🔐 Secure admin login with password hashing  
- 🧾 Add, update, delete, and list student records  
- ✅ Input validation (client-side + server-side)  
- 🎨 Bootstrap 5 UI with responsive layout  
- 🐳 Dockerized for easy deployment  
- 🔄 CSRF protection and form error handling  

---

## 💻 Run Locally Without Docker

### 1. Clone the repository

```bash
git clone https://github.com/Hussain-Ali-12/Flask-Student-Management-System.git
cd Flask-Student-Management-System
```

### 2. Create a virtual environment

```bash
python -m venv env
# Activate:
source env/bin/activate         # On macOS/Linux
env\Scripts\activate            # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask app

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🐳 Run With Docker

### 1. Build Docker image

```bash
docker build -t flask-students-app .
```

### 2. Run container

```bash
docker run -p 5000:5000 flask-students-app
```

Now access the app at: [http://localhost:5000](http://localhost:5000)

### 3. Stop & remove container 

```bash
docker stop flask-students-app
docker rm flask-students-app
```

---

## 📦 Requirements

These are already included in `requirements.txt`, but listed here for clarity:

- Flask  
- Flask-WTF  
- Flask-SQLAlchemy  
- email-validator  
- python-dotenv  
- Werkzeug

To install manually:

```bash
pip install Flask Flask-WTF Flask-SQLAlchemy email-validator python-dotenv
```

---

## 🔐 Security Notes

- Passwords are securely hashed using `werkzeug.security`
- CSRF tokens protect forms via Flask-WTF
- All user inputs validated (HTML5 pattern + backend)
- Emails validated using `email-validator`

---

## 🧪 Admin Flow

1. Register at `/register` (optional depending on setup)  
2. Log in at `/`  
3. Manage students from the dashboard  

---

## 📃 License

MIT License – free to use, modify, and distribute.

---

## 🙋 Need Help?

If you encounter any issues, open a GitHub issue or submit a pull request.
