from flask import Blueprint, render_template, request, redirect, session

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    forums = [
        {'name': 'General Discussion', 'description': 'A place to discuss general topics.', 'forum_id': 1},
        {'name': 'Tech Talk', 'description': 'Discuss the latest in tech.', 'forum_id': 2}
    ]
    return render_template('home.html', forums=forums)

@main.route('/home-ja')
def home_ja():
    forums = [
        {'name': '一般的な議論', 'description': '一般的なトピックについて議論する場所。', 'forum_id': 1},
        {'name': '技術トーク', 'description': '最新の技術について議論する。', 'forum_id': 2}
    ]
    return render_template('home_ja.html', forums=forums)


