from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

    def __init__(self, username, name, email, hash):
        self.username = username
        self.name = name
        self.email = email
        self.hash = hash

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


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


class Save(db.Model):
    __tablename__ = 'saved'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    edit_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    user = db.relationship('User', foreign_keys=user_id)
    category = db.relationship('Category', foreign_keys=category_id)

    def __int__(self, title, link, post_date, edit_date, user_id, category_id):
        self.title = title
        self.link = link
        self.post_date = post_date
        self.edit_date = edit_date
        self.user_id = user_id
        self.category_id = category_id
