# Copyright (c) 2020 samuele
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .app import app
from .blueprints.sessionctrl import blue
from .blueprints.main import main


def launch():
    app.register_blueprint(blue)
    app.register_blueprint(main)
    app.run(debug=True)
