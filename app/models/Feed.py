from app import db


class Feed(db.Model):
    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    portalname = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    update_date = db.Column(db.Date, nullable=False)

    def __init__(self, portalname, url, description, update_date):
        self.portalname = portalname
        self.url = url
        self.description = description
        self.update_date = update_date