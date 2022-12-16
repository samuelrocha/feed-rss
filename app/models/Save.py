from app import db
from datetime import datetime

class Save(db.Model):
    __tablename__ = 'saved'

    id = db.Column(db.Integer, primary_key=True)
    save_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    user = db.relationship('User', foreign_keys=user_id)
    news = db.relationship('New', foreign_keys=news_id)

    def __init__(self, user_id, news_id):
        self.save_date = datetime.now()
        self.user_id = user_id
        self.news_id = news_id