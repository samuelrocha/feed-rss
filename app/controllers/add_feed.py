from app import app, db
from flask import render_template, request, redirect
from app.controllers.helpers import get_xml, apology
from app.models.forms import AddFeedForm
from flask_login import login_required, current_user
from app.models.tables import Category
from datetime import datetime
from app.models.tables import Feed


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_view():

    form = AddFeedForm()

    categories = db.session.execute(
        db.select(Category).order_by(Category.name)).all()
    form.category_id.choices = [
        (category[0].id, category[0].name) for category in categories]

    if request.method == 'POST':

        if form.validate_on_submit():

            try:
                xml = get_xml(form.url.data)
                feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string, datetime.now(), current_user.id, form.category_id.data)
                
                db.session.add(feed)
                db.session.commit()
            except Exception as err:
                print(err)
                return redirect('/add')
            return "OK"


        return apology("Bakka", 400)

    return render_template('add_feed.html', form=form)
