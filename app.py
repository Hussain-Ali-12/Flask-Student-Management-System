from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from forms import StudentForm
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # Set to True for HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Database models
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

# Routes
@app.route('/', methods=['GET'])
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
        return redirect('/login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        new_admin = Admin(username=username, password=password_hash)
        db.session.add(new_admin)
        db.session.commit()
        session['admin'] = username
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
            return redirect('/dashboard')
        return "Invalid credentials. Try again."
    return render_template('login.html')

@csrf.exempt
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'admin' not in session:
        return redirect('/login')
    form = StudentForm()
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
        return redirect('/dashboard')
    students = Students.query.all()
    return render_template('dashboard.html', form=form, students=students)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if 'admin' not in session:
        return redirect('/login')
    student = Students.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('update.html', form=form, student=student)

@app.route('/delete/<int:id>')
def delete(id):
    if 'admin' not in session:
        return redirect('/login')
    student = Students.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
