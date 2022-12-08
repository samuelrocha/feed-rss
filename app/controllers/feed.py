from app import app, db
from flask import render_template, request, redirect
from app.controllers.helpers import get_xml
from app.models.forms import AddFeedForm
from flask_login import login_required, current_user
from app.models.tables import Category
from datetime import datetime
from app.models.tables import Feed
from requests.exceptions import MissingSchema
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


# CREATE
@app.route('/feed/add', methods=['GET', 'POST'])
@login_required
def create_feed():

    form = AddFeedForm()

    categories = db.session.execute(
        db.select(Category).order_by(Category.name)).all()
    form.category_id.choices = [
        (category[0].id, category[0].name) for category in categories]

    if request.method == 'POST':

        if form.validate_on_submit():

            try:
                xml = get_xml(form.url.data)
                feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string,
                            datetime.now(), current_user.id, form.category_id.data)

                db.session.add(feed)
                db.session.commit()
            except MissingSchema:

                """
                    TODO
                    URL INVALIDA

                """
            except AttributeError:

                """
                    TODO
                    XML INCORRETO

                """
                return redirect('/feed/list')
            return redirect('/feed/list')

        """
            TODO
            CATEGORY INVALIDA
        
        """

        return redirect("/feed/list")

    return render_template('feed_add.html', form=form)


# READ
@app.route("/feed/list")
@login_required
def read_feed():

    stmt = select(Feed.id, Feed.portalname, Category.name, Feed.edit_date).join(
        Feed.category).where(Feed.user_id == current_user.id)

    feed = db.session.execute(stmt).all()

    return render_template("feed_list.html", feeds=feed)

# UPDATE
@app.route("/feed/edit/<id>")
def update_feed(id):
    
    smtm = select(Feed).where(Feed.user_id ==
                              current_user.id).where(Feed.id == id)

    try:
        row = db.session.execute(smtm).one()
        feed = row[0]
    except NoResultFound:

        """
            TODO
            EDIT NOT FOUND

        """

    return "WORKING..."

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
