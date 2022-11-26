from flask import Flask, render_template, request, redirect
from module import feed_rss, create_error_image

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
            return redirect('/error')

    return render_template('add.html')


@app.route('/error')
def error():
    img = create_error_image()
    return render_template('error.html', img=img)
