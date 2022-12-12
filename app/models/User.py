from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

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

    @login_manager.user_loader
    def load_user(username):
        return User.query.get(username)

    def get_user_by_username(username):
        smtm = db.select(User).filter_by(username=username)
        user = db.session.execute(smtm).first()
        if user:
            return user[0]
        else:
            return False

    def create_user(form):

        hash = generate_password_hash(form.password.data)
        user = User(form.username.data, form.name.data,
                        form.email.data, hash)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError:
            return False

    def check_password(form):
        user = User.get_user_by_username(form.username.data)
        if check_password_hash(user.hash, form.password.data):
            return user
        else:
            return False
