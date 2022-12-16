from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, URLField, TextAreaField, DateTimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(
        6, 21, "At least 6 characters, maximum 21")])
    password = PasswordField('Password', [InputRequired(), Length(
        8, 21, "At least 8 characters, maximum 21")])

class RegisterForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(
        6, 21, "At least 6 characters, maximum 21")])
    name = StringField('Nickname', [InputRequired(), Length(
        3, 50, "At least 3 characters, maximum 50")])
    email = StringField('E-mail', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(), EqualTo(
        'confirm', 'Password must be match'), Length(8, 21, "At least 8 characters, maximum 21")])
    confirm = PasswordField('Repeat Password', [InputRequired(), Length(
        8, 21, "At least 8 characters, maximum 21")])


class AddFeedForm(FlaskForm):
    url = URLField('URL', [InputRequired(), Length(max=250)])
    list_id = SelectField('List', [InputRequired()], coerce=int)


class EditFeedForm(FlaskForm):
    id = StringField("Id")
    portalname = StringField("Portalname", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    url = URLField('URL', [InputRequired(), Length(max=250)])
    list_id = SelectField('List', [InputRequired()], coerce=int)


class EditNicknameForm(FlaskForm):
    name = StringField('Nickname', [InputRequired(), Length(
        3, 50, "At least 3 characters, maximum 50")])

class EditEmailForm(FlaskForm):
    email = StringField('E-mail', [InputRequired(), Email()])

class EditPasswordForm(FlaskForm):
    password = PasswordField('Password', [InputRequired(), EqualTo(
        'confirm', 'Password must be match'), Length(8, 21, "At least 8 characters, maximum 21")])
    confirm = PasswordField('Repeat Password', [InputRequired(), Length(
        8, 21, "At least 8 characters, maximum 21")])
