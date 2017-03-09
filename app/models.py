
from hashlib import md5
from app import db


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255), index=True, unique=True)
    nickname = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='users', cascade="all, delete-orphan", lazy='dynamic')

    def avatar(self, size):
        return 'https://pickaface.net/assets/images/slides/slide4.png'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email):
        self.username = username
        self.email = email

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
            version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
             break
            version += 1
            return new_nickname


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)

    def __init__(self,post):
        self.post= post

    def __repr__(self):
        return '<Post %r>' % (self.body)
