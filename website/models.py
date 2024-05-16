from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func

Forum_user = db.Table(
    "forum_teachers",
    db.Column("user_id", db.Integer, db.ForeignKey("users.user_id")),
    db.Column(
        "forum_id",
        db.Integer,
        db.ForeignKey("forums.forum_id"),
    ),
)


class Role(db.Model):
    __tablename__ = "roles"

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.role_name = name

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True)

    users = db.relationship("User", backref="role")

    def __repr__(self):
        return f"id: {self.role_id}, type: {self.role_name}"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, email, name, password, school, birthday, role_id):
        self.email = email
        self.name = name
        self.password = password
        self.school = school
        self.birthday = birthday
        self.role_id = role_id

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    school = db.Column(db.String(150))
    birthday = db.Column(db.Date)

    role_id = db.Column(db.ForeignKey("roles.role_id"))

    def __repr__(self):
        return f"id: {self.user_id}, email: {self.email}, name: {self.name}, school: {self.school}, birthday: {self.birthday}, role: {self.role_id}"


class Forum(db.Model):
    __tablename__ = "forums"

    def __init__(self, name):
        self.name = name

    forum_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    users = db.relationship("User", secondary=Forum_user, backref="forums")

    def __repr__(self):
        return f"id: {self.forum_id}, name: {self.name}"


class Post(db.Model):
    __tablename__ = "posts"

    def __init__(self, title, tag, content, date, user_id, forum_id):
        self.title = title
        self.tag = tag
        self.content = content
        self.likes = 0
        self.date = date
        self.report = False
        self.user_id = user_id
        self.forum_id = forum_id

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    tag = db.Column(db.String(20))
    content = db.Column(db.String(300))
    likes = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    report = db.Column(db.Boolean)

    user_id = db.Column(db.ForeignKey("users.user_id"))
    forum_id = db.Column(db.ForeignKey("forums.forum_id"))

    user = db.relationship("User", backref="posts")
    forum = db.relationship("Forum", backref="posts")

    def __repr__(self):
        return f"id: {self.post_id}, title: {self.title}, tag: {self.tag}, content: {self.content}, likes: {self.likes}, date: {self.date}, report: {self.report}, user_id: {self.user_id}, forum_id: {self.forum_id}"


class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))

    user_id = db.Column(db.ForeignKey("users.user_id"))
    post_id = db.Column(db.ForeignKey("posts.post_id"))

    user = db.relationship("User", backref="comments")
    post = db.relationship("Post", backref="comments")
