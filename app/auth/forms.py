from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(message="Username cannot be empty!")])
	password = PasswordField('Password', validators=[InputRequired(message="Password cannot be empty!")])
	redirect = HiddenField()
	submit = SubmitField('Sign In')