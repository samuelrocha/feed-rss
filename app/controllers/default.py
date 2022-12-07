from app import app, db, login_manager
from flask import render_template, request, redirect
from app.controllers.helpers import feed_rss, apology
from app.models.forms import LoginForm, RegisterForm, AddFeedForm
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.tables import User
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import NoResultFound, IntegrityError


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@app.route('/')
@login_required
def index():
    feed = feed_rss('https://diolinux.com.br/feed')
    return render_template('index.html', feed=feed)


@app.route('/login', methods=['GET', 'POST'])
def login():

    logout_user()
    msg = None
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            try:
                user = db.session.execute(
                    db.select(User).filter_by(username=form.username.data)).one()

                if check_password_hash(user[0].hash, form.password.data):
                    login_user(user[0])
                    return redirect('/')

            except NoResultFound:
                pass

            msg = "incorrect username or password"

    return render_template('login.html', form=form, msg=msg)


@app.route('/logout')
def logout():

    logout_user()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = None
    logout_user()
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            hash = generate_password_hash(form.password.data)
            user = User(form.username.data, form.name.data,
                        form.email.data, hash)

            try:
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect('/')

            except IntegrityError:
                db.session.rollback()

            msg = 'username or email already exists'

    return render_template('register.html', form=form, msg=msg)

@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return apology(e.name, e.code)
