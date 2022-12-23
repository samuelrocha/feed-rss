from app import app, db
from flask import render_template, redirect
from app.models.forms import LoginForm, RegisterForm, EditNicknameForm, EditEmailForm, EditPasswordForm
from app.models.User import User
from flask_login import login_user, logout_user, current_user, login_required
from app.models.List import List


@app.get('/login')
def login_get():

    logout_user()
    form = LoginForm()
    return render_template('login.html', form=form)


@app.post('/login')
def login_post():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.check_password(form)
        if user:
            login_user(user)
            return redirect('/news')
        else:
            return "PASSWORD INCORRETO"

    return "FORMULARIO INVALIDO"


@app.get('/logout')
def logout_get():

    logout_user()
    return redirect('/login')


@app.get('/register')
def register_get():

    logout_user()
    form = RegisterForm()

    return render_template('register.html', form=form)


@app.post('/register')
def register_post():

    form = RegisterForm()

    if form.validate_on_submit():

        user = User.create_user(form)
        if user:
            login_user(user)
            l = List('General', current_user.id)
            db.session.add(l)
            db.session.commit()
            return redirect('/news')
        else:
            return "USUÁRIO JÁ EXISTE"

    return "FORMULARIO INVALIDO"


@app.get('/profile')
@login_required
def profile_get():
    return render_template('profile.html')


@app.get('/profile/edit/nickname')
@login_required
def edit_nickname_get():

    form = EditNicknameForm()

    return render_template('edit_nickname.html', form=form)


@app.post('/profile/edit/nickname')
@login_required
def edit_nickname_post():

    form = EditNicknameForm()

    if form.validate_on_submit():

        current_user.name = form.name.data
        User.update_user()

        return redirect('/profile')

    return 'NICKNAME INCORRETO'


@app.get('/profile/edit/email')
@login_required
def edit_email_get():

    form = EditEmailForm()

    return render_template('edit_email.html', form=form)


@app.post('/profile/edit/email')
@login_required
def edit_email_post():

    form = EditEmailForm()

    if form.validate_on_submit():

        current_user.email = form.email.data
        if User.update_user():
            return redirect('/profile')
        return 'EMAIL JÁ EXISTE'

    return 'EMAIL INCORRETO'


@app.get('/profile/edit/password')
@login_required
def edit_password_get():

    form = EditPasswordForm()

    return render_template('edit_password.html', form=form)


@app.post('/profile/edit/password')
@login_required
def edit_password_post():

    form = EditPasswordForm()

    if form.validate_on_submit():

        User.update_password(current_user, form.password.data)

        return redirect('/logout')

    return "SENHAS DIFERENTES"
