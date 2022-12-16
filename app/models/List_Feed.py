from app import db

class List_Feed(db.Model):
    __tablename__ = 'lists_feeds'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    list = db.relationship('List', foreign_keys=list_id)
    feed = db.relationship('Feed', foreign_keys=feed_id)

    def __init__(self, list_id, feed_id):
        self.list_id = list_id
        self.feed_id = feed_id