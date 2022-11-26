from flask import Flask, render_template, request, redirect
from module import feed_rss, apology


app = Flask(__name__)


@app.route('/')
def index():
    feed = feed_rss('https://diolinux.com.br/feed')
    return render_template('index.html', feed=feed)


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
