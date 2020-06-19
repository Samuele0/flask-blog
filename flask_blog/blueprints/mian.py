from flask import Blueprint, render_template, session

main = Blueprint("main", __name__)


@main.route("/")
def home():
    logged = False
    if "username" in session:
        logged = True
    return render_template("index.html",
                           logged=logged,
                           start_page=1,
                           end_page=6,
                           curr_page=2,
                           posts=[
                               {
                                   'id': 543,
                                   'img': 'https://via.placeholder.com/150',
                                   'title': 'Title of the first post! this title can be fairly long;but not too much',
                                   'content': "asdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
                               }
                           ])
