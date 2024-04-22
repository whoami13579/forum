from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class Role(db.Model):
    __tablename__ = "roles"

    # id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.Integer, unique=True, primary_key=True)
    role_name = db.Column(db.String(20), unique=True)

    users = db.relationship("User", backref="role")

    def __repr__(self):
        return str(id) + " " + self.role_type + " " + self.role_name


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    self_introduction = db.Column(db.String(500))

    role_type = db.Column(db.Integer, db.ForeignKey("roles.role_type"))

    def __repr__(self):
        return str(id) + " " + self.user_name
