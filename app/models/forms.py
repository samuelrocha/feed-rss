from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    hash = PasswordField('hash', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')

class AddFeedForm(FlaskForm):
    link = StringField('link', validators=[DataRequired()])
    category = IntegerField('category', validators=[DataRequired()])