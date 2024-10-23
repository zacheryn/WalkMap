"""
MDE index view.

URLs include:
/
"""
import uuid
import pathlib
import hashlib
import flask
import arrow
import MDE


@MDE.app.route('/')
def show_index():
    """Display / route.  Initializes React."""

    # For compilation purposes
    context = {}
    return flask.render_template("index.html", **context)

@MDE.app.route('/user/<username>/')
def user_page(username):

    connection = MDE.model.get_db()

    cur = connection.execute(
        "SELECT user_id, username, first_name, last_name, [filename] "
        "FROM Users "
        "WHERE username = ",
        (username)
    )

    users = cur.fetchall()
    user_exists = len(users) > 0
    user_picture = users[0][4]
    uid = users[0][0]

    # get reviews
    '''cur = connection.execute(
        "SELECT user_id, username, first_name, last_name, [filename] "
        "FROM Users "
        "WHERE username = ",
        (username, )
    )'''

    context = {"username": username, "exists":user_exists}
    return flask.render_template("user.html", **context)

