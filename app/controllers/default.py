from app import app, db, login_manager
from flask import render_template, request, redirect
from app.controllers.helpers import feed_rss, apology
from app.models.forms import LoginForm
from werkzeug.exceptions import HTTPException
from app.models.tables import User
from flask_login import login_user, logout_user, login_required


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
@login_required
def index():
    feed = feed_rss('https://diolinux.com.br/feed')
    return render_template('index.html', feed=feed)


@app.route('/logout')
def test():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.execute(
                db.select(User).filter_by(username=form.username.data)).one()

            if user[0] and user[0].hash == form.hash.data:
                login_user(user[0])
                return redirect('/')
            else:
                return redirect('/login')
        else:
            return [form.username.errors, form.hash.errors]
    return render_template('login.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_view():
    if request.method == 'POST':

        name = request.form['name']
        url = request.form['url']
        category = request.form['category']

        if not name or not url or not category:
            return apology("fill in all fields", 400)

    return render_template('add.html')


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return apology(e.name, e.code)