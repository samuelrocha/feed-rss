from app import db
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from app.models.Category import Category
from app.controllers.helpers import get_xml
from datetime import datetime
from flask_login import current_user


class Feed(db.Model):
    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    portalname = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    edit_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    user = db.relationship('User', foreign_keys=user_id)
    category = db.relationship('Category', foreign_keys=category_id)

    def __init__(self, portalname, url, description, edit_date, user_id, category_id):
        self.portalname = portalname
        self.url = url
        self.description = description
        self.edit_date = edit_date
        self.user_id = user_id
        self.category_id = category_id

    def get_feed_by_id(id):
        smtm = select(Feed).where(Feed.id == id).where(
            Feed.user_id == current_user.id)
        
        row = db.session.execute(smtm).first()
        if row:
            return row[0]
        else:
            return False

    def get_feed():
        stmt = select(Feed.id, Feed.portalname, Feed.url, Category.name, Feed.edit_date).join(
            Feed.category).where(Feed.user_id == current_user.id)

        feed = db.session.execute(stmt).all()
        return feed

    def get_newsfeed():
        row = Feed.get_feed()
        items = []
        for feed in row:
            xml = get_xml(feed.url)
            for item in xml.find_all('item'):
                pub_date = datetime.strptime(
                item.pubDate.string, "%a, %d %b %Y %H:%M:%S %z")
                items.append({
                        'title': item.title.string,
                        'link': item.link.string,
                        'portalname': feed.portalname,
                        'category': feed.name,
                        'post_date': pub_date
                })
        return items

    def delete_feed(id):

        feed = Feed.get_feed_by_id(id)
        if feed:
            db.session.delete(feed)
            db.session.commit()
            return True
        else:
            return False

    def create_feed(form):
        xml = get_xml(form.url.data)
        try:
            feed = Feed(xml.channel.title.string, form.url.data, xml.channel.description.string,
                        datetime.now(), current_user.id, form.category_id.data)
            db.session.add(feed)
            db.session.commit()
            return True
        except AttributeError:
            return False

    def update_feed(id, form):

        feed = Feed.get_feed_by_id(id)
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
            return True
        return False