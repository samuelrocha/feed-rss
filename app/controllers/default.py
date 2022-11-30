from app import app
from flask import render_template, request, url_for
from app.controllers.module import feed_rss, apology
from app.models.forms import LoginForm


@app.route('/')
def index():
    feed = feed_rss('https://diolinux.com.br/feed')
    return render_template('index.html', feed=feed)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return "YES BABY"
        else:
            return apology('bakka',404)
    return render_template('login.html', form=form)

@app.route('/add', methods=['GET', 'POST'])
def add_view():
    if request.method == 'POST':

        name = request.form['name']
        url = request.form['url']
        category = request.form['category']

        if not name or not url or not category:
            return apology("fill in all fields", 400)

    return render_template('add.html')


@app.route('/error')
def error():
    return apology('Congratulations, you know how to use the URL', 400)


@app.route('/test')
def test():
    return 'OK'