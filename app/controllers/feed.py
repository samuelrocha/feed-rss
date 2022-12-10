from app import app, db
from flask import render_template, request, redirect
from app.controllers.helpers import get_xml, get_feed
from app.models.forms import AddFeedForm, EditFeedForm
from flask_login import login_required, current_user
from app.models.tables import Category
from datetime import datetime
from app.models.tables import Feed
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


# CREATE
@app.route('/feed/add', methods=['GET', 'POST'])
@login_required
def create_feed():

    form = AddFeedForm()

    categories = db.session.execute(
        select(Category).order_by(Category.name)).all()
    form.category_id.choices = [
        (category[0].id, category[0].name) for category in categories]

    if request.method == 'POST':

        if form.validate_on_submit():
            xml = get_xml(form.url.data)
            try:
                feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string,
                            datetime.now(), current_user.id, form.category_id.data)

                db.session.add(feed)
                db.session.commit()
                return redirect('/feed/list')
            except AttributeError:

                """
                    TODO
                    XML INCORRETO

                """
                return "XML INCORRETO"

        """
            TODO
            USUARIO ALTEROU O INPUT
        
        """

        return "USUARIO ALTEROU O INPUT"

    return render_template('feed_add.html', form=form)


# READ
@app.route("/feed")
@app.route("/feed/list")
@login_required
def read_feed():

    stmt = select(Feed.id, Feed.portalname, Category.name, Feed.edit_date).join(
        Feed.category).where(Feed.user_id == current_user.id)

    feed = db.session.execute(stmt).all()
    return render_template("feed_list.html", feeds=feed)


# UPDATE
@app.route("/feed/edit", methods=["POST"])
@app.route("/feed/edit/<id>", methods=["GET", "POST"])
@login_required
def update_feed(id=None):

    form = EditFeedForm()

    if request.method == "POST":

        smtm = select(Feed).where(Feed.user_id ==
                                  current_user.id).where(Feed.id == form.id.data)

        feed = get_feed(smtm)
        feed = feed[0][0]
        if feed:
            feed.url = form.url.data
            feed.category_id = form.category_id.data
            feed.edit_date = datetime.now()
            
            xml = get_xml(feed.url)

            try:
                feed.portalname = xml.channel.title.string
                feed.description = xml.channel.description.string
            except AttributeError:
                pass

            db.session.commit()

            return redirect("/feed/list")

        """
            TODO
            USER MODIFY ID ERROR

        """
        return "USER MODIFY ID ERROR"

    smtm = select(Feed).where(Feed.user_id ==
                              current_user.id).where(Feed.id == id)

    feed = get_feed(smtm)
    feed = feed[0][0]
    if feed:
        categories = db.session.execute(
            select(Category).order_by(Category.name)).all()

        form.id.data = id
        form.portalname.data = feed.portalname
        form.description.data = feed.description
        form.url.data = feed.url
        form.category_id.choices = [
            (category[0].id, category[0].name) for category in categories]
        form.category_id.data = feed.category_id

        return render_template("feed_edit.html", form=form)
    """
            TODO
            USER MODIFY ID ERROR

    """
    return "USER MODIFY ID ERROR"


# DELETE
@app.route('/feed/remove/<id>')
@login_required
def delete_feed(id):

    smtm = select(Feed).where(Feed.user_id ==
                              current_user.id).where(Feed.id == id)

    try:
        row = db.session.execute(smtm).one()
        feed = row[0]
        db.session.delete(feed)
        db.session.commit()
    except NoResultFound:

        """
            TODO
            REMOVE NOT FOUND

        """

    return redirect('/feed/list')
