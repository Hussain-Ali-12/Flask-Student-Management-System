from app import db, Admin
from app import app
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # Create a default admin if not already exists
    if not Admin.query.first():
        admin = Admin(username="admin", password=generate_password_hash("admin"))
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")

    print("✅ Database and tables ready!")
