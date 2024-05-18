from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Role, User, Forum
from . import db
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user, forums=Forum.query.filter_by().all())
