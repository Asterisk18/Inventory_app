from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField , IntegerField
from wtforms.validators import DataRequired , Length, Email, EqualTo, ValidationError , NumberRange
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired() , Length(5,20)])
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("username not available")
        
    def validate_email(self , email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError("email already registered, try logging in")


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class ItemForm(FlaskForm):
    name = StringField('Item Name' , validators=[DataRequired()])
    quantity = IntegerField('Quantity' , validators=[DataRequired() , NumberRange(min=0)])
    submit = SubmitField('Submit')