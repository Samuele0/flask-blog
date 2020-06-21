# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Blueprint, request, render_template, Response, abort, redirect, session, url_for
from ..database_model import User, db
from random import getrandbits
from hashlib import md5

blue = Blueprint("sessionctrl", __name__)


@blue.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
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
        resp: Response = redirect(url_for('sessionctrl.login'))
        resp.delete_cookie("csrf")
    csrf = getrandbits(64)
    resp = Response(render_template('register.html', csrf=csrf))
    resp.set_cookie('csrf', str(csrf))
    return resp


@blue.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main.home"))


@blue.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password: str = request.form["password"]
        csrf_form = request.form["csrf"]
        csrf_cookie = request.cookies.get("csrf")
        if csrf_form != csrf_cookie:
            return abort(400, "CSRF Token mismatch")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "Wrong User or password", 400
        found_password = user.password
        salt = user.salt
        salted_password = bytes(
            [b1 ^ b2 for b1, b2 in zip(password.encode(), salt)])
        if md5(salted_password).hexdigest() != found_password:
            return "User or Password"
        session["username"] = username
        session["userid"] = user.id
        return redirect(url_for('main.home'))
    csrf = getrandbits(64)
    resp = Response(render_template('login.html', csrf=csrf))
    resp.set_cookie('csrf', str(csrf))
    return resp
