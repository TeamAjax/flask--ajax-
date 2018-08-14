from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('username', validators=[Regexp('([a-z|_]+)'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SigninForm(FlaskForm):
    username = StringField('username', validators=[ Regexp('([a-z|_]+)'), DataRequired()])
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[Email(), Regexp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'), DataRequired()])
    phone = StringField('phone', validators=[Regexp('()'), DataRequired()])
    password = PasswordField('password', validators=[Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$'), DataRequired()])
    password_confirm = PasswordField('password confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')