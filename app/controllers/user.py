from app import app
from flask import render_template, redirect
from app.models.forms import LoginForm, RegisterForm
from app.models.User import User
from flask_login import login_user, logout_user


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
            return redirect('/newsfeed')
        else:
            return "PASSWORD INCORRETO"


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
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        user = User.create_user(form)
        if user:
            login_user(user)
            return redirect('/newsfeed')
        else:
            return "USUÁRIO JÁ EXISTE"
