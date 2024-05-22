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


@views.route("/forum/<forum_id>/join")
@login_required
def join_forum(forum_id):
    forum = Forum.query.filter_by(forum_id=forum_id).first()
    forum.users.append(current_user)

    db.session.commit()
    flash("Join", category="success")

    return redirect(url_for("views.forum", forum_id=forum_id))


@views.route("/forum/<forum_id>/leave")
@login_required
def leave_forum(forum_id):
    forum = Forum.query.filter_by(forum_id=forum_id).first()
    forum.users.remove(current_user)

    db.session.commit()
    flash("Leave", category="success")

    return redirect(url_for("views.forum", forum_id=forum_id))


@views.route("/new-forum", methods=["GET", "POST"])
@login_required
def new_forum():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if Forum.query.filter_by(name=name).first():
            flash("Forum already exists", category="error")
            return redirect(url_for("views.new_forum"))

        forum = Forum(name, description, current_user.get_id())
        forum.users.append(current_user)

        db.session.add(forum)
        db.session.commit()

        flash("New Forum Created", category="success")
        return redirect(url_for("views.home"))

    return render_template("new_forum.html", user=current_user)


@views.route("/forum/<forum_id>/delete")
@login_required
def delete_forum(forum_id):
    forum = Forum.query.filter_by(forum_id=forum_id).first()

    if forum.user_id == current_user.get_id() or current_user.get_id() == 2:
        db.session.delete(forum)
        db.session.commit()

        flash("Forum Deleted", category="success")
        return redirect(url_for("views.home"))


    flash("You can't delete this forum.", category="error")
    return redirect(url_for("views.homne"))

@views.route("/my-forums")
@login_required
def my_forums():
    return render_template("my_forums.html", user=current_user, forums=current_user.forums)
    

@views.route("/forum/<forum_id>/<post_id>")
@login_required
def view_post(forum_id, post_id):
    return render_template("post.html", user=current_user, post=Post.query.filter_by(post_id=post_id).first())
