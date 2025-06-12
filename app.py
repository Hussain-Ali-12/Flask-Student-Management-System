from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from forms import StudentForm
from dotenv import load_dotenv
from uuid import uuid4
import os
import logging

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# App configuration
# =========================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)

# =========================
# Initialize extensions
# =========================
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# =========================
# Configure logging
# =========================
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/errors.log',
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)

# =========================
# Database models
# =========================
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))
    email = db.Column(db.String(100))

# =========================
# Routes
# =========================

@app.route('/')
def index():
    return render_template('index.html')


@csrf.exempt
@app.route('/go-to-dashboard', methods=['POST'])
def go_to_dashboard():
    if 'admin' in session:
        return redirect('/dashboard')
    return redirect('/login')


@csrf.exempt
@app.route('/register', methods=['GET', 'POST'])
def register():
    if Admin.query.first():
        flash("Admin already registered. Please log in.", "info")
        return redirect('/login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        new_admin = Admin(username=username, password=password_hash)
        db.session.add(new_admin)
        db.session.commit()
        session['admin'] = username
        flash("Admin account created successfully! You are now logged in.", "success")
        return redirect('/dashboard')
    return render_template('register.html')


@csrf.exempt
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not Admin.query.first():
        return redirect('/register')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin'] = username
            flash("Login successful!", "success")
            return redirect('/dashboard')
        flash("Invalid username or password. Please try again.", "danger")
    return render_template('login.html')


@csrf.exempt
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    flash("You have been logged out.", "info")
    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'admin' not in session:
        flash("Unauthorized access. Please log in.", "warning")
        return redirect('/login')

    form = StudentForm()
    error_id = str(uuid4())[:8]

    try:
        if form.validate_on_submit():
            new_student = Students(
                fname=form.fname.data,
                lname=form.lname.data,
                age=form.age.data,
                city=form.city.data,
                email=form.email.data
            )
            db.session.add(new_student)
            db.session.commit()
            flash("Student added successfully!", "success")
            return redirect('/dashboard')

        students = Students.query.all()
        return render_template('dashboard.html', form=form, students=students)

    except Exception as e:
        db.session.rollback()
        logging.error(f"[{error_id}] Error in dashboard route: {e}")
        flash(f"An error occurred while processing your request. Error ID: {error_id}", "danger")
        return render_template("error.html", code=500, message="Something went wrong.", error_id=error_id), 500


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if 'admin' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect('/login')

    student = Students.query.get_or_404(id)
    form = StudentForm(obj=student)

    try:
        if form.validate_on_submit():
            form.populate_obj(student)
            db.session.commit()
            flash("Student record updated successfully!", "success")
            return redirect('/dashboard')
    except Exception as e:
        db.session.rollback()
        error_id = str(uuid4())[:8]
        logging.error(f"[{error_id}] Error updating student ID {id}: {e}")
        flash(f"Update failed. Error ID: {error_id}", "danger")
        return render_template("error.html", code=500, message="Update operation failed.", error_id=error_id), 500

    return render_template('update.html', form=form, student=student)


@app.route('/delete/<int:id>')
def delete(id):
    if 'admin' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect('/login')

    student = Students.query.get_or_404(id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student record deleted successfully.", "warning")
    except Exception as e:
        db.session.rollback()
        error_id = str(uuid4())[:8]
        logging.error(f"[{error_id}] Error deleting student ID {id}: {e}")
        flash(f"Delete failed. Error ID: {error_id}", "danger")
        return render_template("error.html", code=500, message="Delete operation failed.", error_id=error_id), 500

    return redirect('/dashboard')


# =========================
# Error Handlers
# =========================

@app.errorhandler(404)
def not_found(e):
    error_id = str(uuid4())[:8]
    logging.error(f"[{error_id}] 404 Error: {e}")
    flash(f"404 Not Found — Error ID: {error_id}", "danger")
    return render_template("error.html", code=404, message="The requested page does not exist.", error_id=error_id), 404


@app.errorhandler(500)
def server_error(e):
    error_id = str(uuid4())[:8]
    logging.error(f"[{error_id}] 500 Server Error: {e}")
    flash(f"500 Server Error — Error ID: {error_id}", "danger")
    return render_template("error.html", code=500, message="An internal error occurred.", error_id=error_id), 500

# =========================
# Session Management
# =========================

@app.route('/refresh-session', methods=['POST'])
def refresh_session():
    if 'admin' in session:
        session.modified = True  # Updates session timestamp
        return '', 204  # No content
    return '', 401  # Unauthorized

# =========================
# Run the App
# =========================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
