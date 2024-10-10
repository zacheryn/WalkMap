"""
Insta485 index (main) view.

URLs include:
/
"""
import uuid
import pathlib
import hashlib
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    # Check if a user is logged in
    sc_name = insta485.app.config['SESSION_COOKIE_NAME']
    if sc_name not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    logname = flask.session[sc_name]

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT username, filename "
        "FROM users "
    )
    users = cur.fetchall()

    cur = connection.execute(
        "SELECT owner, filename, created, postid "
        "FROM posts "
    )
    posts = cur.fetchall()

    cur = connection.execute(
        "SELECT owner, postid, created, text  "
        "FROM comments "
    )
    comments = cur.fetchall()

    cur = connection.execute(
        "SELECT owner, postid  "
        "FROM likes "
    )
    likes_dq = cur.fetchall()

    # cur = connection.execute(
    #     "SELECT username1, username2  "
    #     "FROM following "
    #     "WHERE username1 = ?",
    #     (logname, )
    # )
    following = insta485.model.get_user_following(connection, logname)

    # Format followers list before templating
    temp_follow = []
    for folling in following:
        if folling["username1"] == logname:
            temp_follow.append(folling["username2"])

    # Humanize time before templating
    for post in posts:
        post["created"] = arrow.get(post["created"]).humanize()

    user_likes = []
    for like in likes_dq:
        if like["owner"] == logname:
            user_likes.append(like["postid"])

    # Add database info to context
    context = {"users": users, "posts": posts,
               "logname": logname, "comments": comments,
               "likes": likes_dq, "following": temp_follow,
               "user_likes": user_likes}
    return flask.render_template("index.html", **context)
