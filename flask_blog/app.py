# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:changeme@localhost/postgres"
app.secret_key = b'\x9b\xcf\x1d\x1f4sN\xaa\xb31\x89F\xa4\xe5\x1dK'

