from flask import Blueprint, redirect, url_for, render_template, session, request
from ..database_model import db, Post
main = Blueprint("main", __name__)


@main.route("/")
def home():
    logged = False
    if "username" in session:
        logged = True
    current_page = int(request.args.get("page", default="1"))
    previous_page = max(1, current_page-2)
    pages = Post.query.paginate(current_page, 10)
    end_page = min(max(1, pages.pages), previous_page+5)

    return render_template("index.html",
                           logged=logged,
                           posts=pages.items,
                           start_page=previous_page,
                           end_page=end_page+1,
                           curr_page=current_page)


@main.route("/newpost", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        username = session["username"]
        userid = session["userid"]
        image = request.form["image"]
        title = request.form["title"]
        content = request.form["content"]

        post = Post(
            image=image,
            title=title,
            content=content,
            author_name=username,
            author=int(userid)
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("new_post.html")


@main.route("/post/<id>")
def post(id):
    post = Post.query.get(int(id))
    return render_template("post.html", post=post)
