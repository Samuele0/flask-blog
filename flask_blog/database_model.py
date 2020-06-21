# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(40))
    salt = db.Column(db.LargeBinary())
    addresses = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80))
    title = db.Column(db.String(200))
    content = db.Column(db.Text())
    author_name = db.Column(db.String(80))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))



db.create_all()
