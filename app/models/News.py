from app import db

class New(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    feed = db.relationship('Feed', foreign_keys=feed_id)

    def __init__(self, title, url, post_date, feed_id):
        self.title = title
        self.url = url
        self.post_date = post_date
        self.feed_id = feed_id