from app import db

class Save(db.Model):
    __tablename__ = 'saved'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    edit_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    user = db.relationship('User', foreign_keys=user_id)
    feed = db.relationship('Feed', foreign_keys=feed_id)

    def __init__(self, title, link, post_date, edit_date, user_id, feed_id):
        self.title = title
        self.link = link
        self.post_date = post_date
        self.edit_date = edit_date
        self.user_id = user_id
        self.feed_id = feed_id

    def commit_save(self):
        db.session.add(self)
        db.session.commit()