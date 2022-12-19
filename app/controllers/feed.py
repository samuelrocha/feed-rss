from app import app, db
from flask import render_template, request, redirect
from app.models.forms import AddFeedForm, EditFeedForm
from flask_login import login_required, current_user
from datetime import timezone, timedelta
from app.models.List import List
from app.models.Feed import Feed
from app.models.List_Feed import List_Feed
from app.models.User import User
from app.models.News import News
from app.controllers.helpers import get_xml
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter
from app.controllers.helpers import apology, PER_PAGE


# CREATE
@app.route('/feed/add', methods=['GET', 'POST'])
@login_required
def add_feed():

    form = AddFeedForm()

    smtm = db.select(List.id, List.name).where(List.user_id == current_user.id)
    lists = db.session.execute(smtm).all()
    form.list_id.choices = [(item.id, item.name) for item in lists]

    if request.method == 'POST':

        if form.validate_on_submit():

            smtm = db.select(Feed.id).where(Feed.url == form.url.data)
            feed_id = db.session.execute(smtm).first()
            if not feed_id:
                xml = get_xml(form.url.data)
                try:
                    feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string,datetime.now())
                    db.session.add(feed)
                    db.session.commit()
                    feed_id = feed.id
                    for item in xml.find_all('item'):
                        pub_date = datetime.strptime(item.pubDate.string, "%a, %d %b %Y %H:%M:%S %z")
                        news = News(item.title.string, item.link.string, pub_date, feed_id)

                        smtm = db.select(News).where(News.url == news.url)
                        old_news = db.session.execute(smtm).first()

                        if not old_news:
                            db.session.add(news)

                except AttributeError:
                    return "INCORRECT XML"
            else:
                feed_id = feed_id[0]

            smtm = db.select(List_Feed.id).where(List_Feed.list_id == form.list_id.data).where(List_Feed.feed_id == feed_id)
            list_feed_id = db.session.execute(smtm).first()

            if not list_feed_id:

                list_feed = List_Feed(form.list_id.data, feed_id)
                db.session.add(list_feed)
                db.session.commit()
            else:
                return "FEED JÁ EXISTE NA LISTA"

        return redirect('/feed/list')

    return render_template('feed_add.html', form=form)


# READ
@app.get("/feed/list")
@login_required
def list_feed():

    smtm = db.select(Feed, List, List_Feed).join(List_Feed.list).join(List_Feed.feed).where(List.user_id == current_user.id)
    feeds = db.session.execute(smtm).all()

    length = len(feeds)

    search = False
    q = request.args.get('q')
    if q:
        search = True


    page = request.args.get(get_page_parameter(), type=int, default=1)

    last_page = length // PER_PAGE + 1
    if page > last_page:
        return apology('Not Found', 404)

    i = (page-1)*PER_PAGE
    feeds = feeds[i:i+PER_PAGE]
    pagination = Pagination(page=page, total=length, search=search, record_name='feeds', per_page=PER_PAGE)

    return render_template("feed_list.html", feeds=feeds, pagination=pagination)

# UPDATE
@app.route("/feed/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_feed(id=None):

    form = EditFeedForm()

    if request.method == "POST":

        smtm = db.select(Feed.id).where(Feed.url == form.url.data)
        feed_id = db.session.execute(smtm).first()
        if not feed_id:
            xml = get_xml(form.url.data)
            try:
                feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string,datetime.now())
                db.session.add(feed)
                db.session.commit()
                feed_id = feed.id
            except AttributeError:
                return "INCORRECT XML"
        else:
            feed_id = feed_id[0]

        
        smtm = db.select(List_Feed.id).where(List_Feed.list_id == form.list_id.data).where(List_Feed.feed_id == feed_id)
        list_feed_id = db.session.execute(smtm).first()

        if not list_feed_id:
            smtm = db.select(List_Feed).where(List_Feed.id == id)
            list_feed = db.session.execute(smtm).first()
            list_feed = list_feed[0]

            list_feed.feed_id = feed_id
            list_feed.list_id = form.list_id.data

            db.session.commit()

            return redirect('/feed/list')
        else:
            return "FEED JÁ EXISTE NA LISTA"


    smtm = db.select(Feed, List_Feed).join(List_Feed.list).join(List.user).join(List_Feed.feed).where(User.id == current_user.id).where(List_Feed.id == id)
    feed = db.session.execute(smtm).first()

    if feed:

        smtm = db.select(List).join(List.user).where(User.id == current_user.id)
        lists = db.session.execute(smtm).all()

        form.id.data = id
        form.portalname.data = feed[0].portalname
        form.description.data = feed[0].description
        form.url.data = feed[0].url
        form.list_id.choices = [
            (item[0].id, item[0].name) for item in lists]
        form.list_id.data = feed[1].list_id

        return render_template("feed_edit.html", form=form)

    return "USER MODIFY ID ERROR"


# DELETE
@app.get('/feed/remove/<id>')
@login_required
def remove_feed(id):

    smtm = db.select(List_Feed).join(List_Feed.list).join(List.user).where(User.id == current_user.id).where(List_Feed.id == id)

    list_feed = db.session.execute(smtm).first()
    print(list_feed[0])

    db.session.delete(list_feed[0])
    db.session.commit()

    return redirect('/feed/list')