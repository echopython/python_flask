from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


# class Followers(db.Model):
#     __tablename__ = 'followers'
#     follower_id = db.Column(db.Integer,db.ForeignKey('userinfo.id'),primary_key=True)
#     followed_id = db.Column(db.Integer,db.ForeignKey('userinfo.id'),primary_key=True)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('userinfo.id'),primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('userinfo.id'),primary_key=True)
)

class User(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)#autoincrement自增长
    uname = db.Column(db.String(50),nullable=False)
    passwd = db.Column(db.String(50),nullable=False)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    followed = db.relationship('User',
                              secondary=followers,
                              primaryjoin=(followers.c.follower_id == id),
                              secondaryjoin=(followers.c.followed_id == id),
                              backref=db.backref('followers', lazy='dynamic'),
                              lazy='dynamic')

    def __init__(self,*args,**kwargs):
        uname = kwargs.get('uname')
        passwd = kwargs.get('passwd')
        self.uname = uname
        self.passwd = generate_password_hash(passwd)

    def check_password(self,raw_password):
        result = check_password_hash(self.passwd,raw_password)
        return result

    def follow(self,userinfo):
        if not self.is_following(userinfo):
            self.followed.append(userinfo)
            return self
    def unfollow(self,userinfo):
        if self.is_following(userinfo):
            self.followed.remove(userinfo)
            return self
    def is_following(self,userinfo):
        return self.followed.filter(followers.c.followed_id==userinfo.id).count() > 0

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('userinfo.id'))
    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('userinfo.id'))
    question = db.relationship('Question',backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('answers'))