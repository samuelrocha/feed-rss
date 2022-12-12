from app import db
from sqlalchemy import select

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_category():
        smtm = select(Category).order_by(Category.name)
        row = db.session.execute(smtm).all()
        return row

    def get_category_by_id(id):
        smtm = select(Category.name).where(Category.id == id)
        row = db.session.execute(smtm).one()
        name = row[0]
        return name