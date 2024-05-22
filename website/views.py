from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Role, User, Forum, Post
from . import db
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user, forums=Forum.query.filter_by().all())


@views.route("/forum/<forum_id>")
def forum(forum_id):
    return render_template("forum.html", user=current_user, forum=Forum.query.filter_by(forum_id=forum_id).first())


@views.route("/forum/<forum_id>/new-post", methods=["GET", "POST"])
@login_required
def new_post(forum_id):
    if request.method == "POST":
        title = request.form.get("title")
        tags = request.form.get("tags")
        content = request.form.get("content")

        post = Post(title, tags, content, current_user.get_id(), forum_id)
        post.user = current_user
        post.forum = Forum.query.filter_by(forum_id=forum_id).first()

        db.session.add(post)
        db.session.commit()

        flash("New Post Created", category="success")
        return redirect(url_for("views.forum", forum_id=forum_id))


    return render_template("new_post.html", user=current_user)
