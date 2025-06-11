from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email

class StudentForm(FlaskForm):
    fname = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50),
            Regexp(r'^[A-Za-z]+$', message="First name must contain only letters.")
        ]
    )
    
    lname = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50),
            Regexp(r'^[A-Za-z]+$', message="Last name must contain only letters.")
        ]
    )
    
    age = IntegerField(
        'Age',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=120, message="Age must be between 1 and 120.")
        ]
    )
    
    city = StringField(
        'City',
        validators=[
            DataRequired(),
            Length(max=50),
            Regexp(r'^[A-Za-z ]+$', message="City must contain only letters and spaces.")
        ]
    )
    
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Invalid email address."),
            Length(max=100)
        ]
    )
