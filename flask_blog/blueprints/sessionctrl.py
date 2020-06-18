# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Blueprint, request, Response, abort, redirect, session
from ..database_model import User, db
from random import getrandbits
from hashlib import md5

blue = Blueprint("sessionctrl", __name__)


@blue.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password: str = request.form["password"]
    csrf_form = request.form["csrf"]
    salt = getrandbits(128).to_bytes(16, 'little')
    salted_password = bytes(
        [b1 ^ b2 for b1, b2 in zip(password.encode(), salt)])
    csrf_cookie = request.cookies.get("csrf")
    if csrf_form != csrf_cookie:
        return abort(400, "CSRF Token mismatch")
    user = User(username=username,
                password=md5(salted_password).hexdigest(),
                salt=salt)

    db.session.add(user)
    db.session.commit()
    resp: Response = redirect("/")
    resp.delete_cookie("csrf")
    return resp


@blue.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password: str = request.form["password"]
    csrf_form = request.form["csrf"]
    csrf_cookie = request.cookies.get("csrf")
    if csrf_form != csrf_cookie:
        return abort(400, "CSRF Token mismatch")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "Wrong User or password"
    found_password = user.password
    salt = user.salt
    salted_password = bytes(
        [b1 ^ b2 for b1, b2 in zip(password.encode(), salt)])
    if md5(salted_password).hexdigest() != found_password:
        return "User or Password"
    session["username"] = username
    session["id"] = user.id
    return "success"
