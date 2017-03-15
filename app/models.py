# from app import app
import datetime
from app import db
from sqlalchemy.sql.schema import PrimaryKeyConstraint
import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy


class Followers(db.Model):
    __tablename__='followers'
    __table_args__ = (
        PrimaryKeyConstraint('follower_id', 'followed_id'),
    )
    follower_id = db.Column('follower_id',db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column('followed_id',db.Integer, db.ForeignKey('users.id'))


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255), index=True, unique=True)
    nickname = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='users', cascade="all, delete-orphan", lazy='dynamic',uselist=True)

    followed = db.relationship('User',
                               secondary=Followers.__table__,
                               primaryjoin=(Followers.follower_id == id),
                               secondaryjoin=(Followers.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(Followers.followed_id == user.id).first() > 0

    def followed_posts(self):
        return Post.query.join(Followers, (Followers.followed_id == Post.user_id)).filter(
            Followers.follower_id == self.id).order_by(Post.timestamp.desc()).all()


class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__=['body']

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, body, user_id):
        self.body = body
       # self.post=post
        self.user_id = user_id


