from app import db, Admin
from app import app
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    db.session.commit()
    print("✅ Database and tables ready!")
