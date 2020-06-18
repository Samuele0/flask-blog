# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .app import app
from .blueprints.sessionctrl import blue


def launch():
    app.register_blueprint(blue)
    app.run(debug=True)
