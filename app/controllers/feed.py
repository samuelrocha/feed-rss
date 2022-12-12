from app import app
from flask import render_template, request, redirect
from app.models.forms import AddFeedForm, EditFeedForm
from flask_login import login_required
from app.models.Feed import Feed
from app.models.Category import Category
from datetime import timezone, timedelta


@app.get('/newsfeed')
@login_required
def index():
    diferenca = timedelta(hours=-3)
    fuso = timezone(diferenca)

    items = Feed.get_newsfeed()
    items = sorted(items, key=lambda item: item['post_date'], reverse=True)

    for i, item in enumerate(items):
        brazil_utc = item['post_date'].astimezone(fuso)
        item['post_date'] = brazil_utc.strftime("%H:%M:%S %d/%m/%Y")
    return render_template('index.html', feed=items)


# CREATE
@app.route('/feed/add', methods=['GET', 'POST'])
@login_required
def add_feed():

    form = AddFeedForm()
    categories = Category.get_category()

    form.category_id.choices = [
        (category[0].id, category[0].name) for category in categories]

    if request.method == 'POST':

        if form.validate_on_submit():

            if Feed.create_feed(form):
                return redirect('/feed/list')
            else:
                return "XML INCORRETO"

        return "USUARIO ALTEROU O INPUT"

    return render_template('feed_add.html', form=form)


# READ
@app.get("/feed/list")
@login_required
def read_feed():

    feed = Feed.get_feed()
    return render_template("feed_list.html", feeds=feed)


# UPDATE
@app.route("/feed/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_feed(id=None):

    form = EditFeedForm()

    if request.method == "POST":
        if Feed.update_feed(id, form):
            return redirect("/feed/list")
        else:
            return "USER MODIFY ID ERROR"

    feed = Feed.get_feed_by_id(id)

    if feed:
        categories = Category.get_category()

        form.id.data = id
        form.portalname.data = feed.portalname
        form.description.data = feed.description
        form.url.data = feed.url
        form.category_id.choices = [
            (category[0].id, category[0].name) for category in categories]
        form.category_id.data = feed.category_id

        return render_template("feed_edit.html", form=form)

    return "USER MODIFY ID ERROR"


# DELETE
@app.get('/feed/remove/<id>')
@login_required
def remove_feed(id):

    if Feed.delete_feed(id):
        return redirect('/feed/list')
    else:
        return "ID INCORRETO"
