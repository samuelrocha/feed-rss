from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, URLField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(
        6, 21, "At least 6 characters, maximum 21")])
    password = PasswordField('Password', [InputRequired(), Length(
        8, 21, "At least 8 characters, maximum 21")])
    remember_me = BooleanField('Remember me')
    recaptcha = RecaptchaField()


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
    recaptcha = RecaptchaField()


class AddFeedForm(FlaskForm):
    url = URLField('URL', [InputRequired(), Length(max=250)])
    category_id = SelectField('Category', [InputRequired()], coerce=int)


class EditFeedForm(FlaskForm):
    id = StringField("Id")
    portalname = StringField("Portalname", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    url = URLField('URL', [InputRequired(), Length(max=250)])
    category_id = SelectField('Category', [InputRequired()], coerce=int)


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