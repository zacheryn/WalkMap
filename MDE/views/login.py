"""
Handles user login.
"""
import uuid
import pathlib
import flask
import MDE
import MDE.config
from MDE.views.authorize import is_loggedin, validate_credentials

@MDE.app.route('/login/')
def show_login():
    """Display /login/ route."""
    # Redirect to / if the user is logged in
    logname = is_loggedin()
    if logname != "":
        return flask.redirect(flask.url_for('show_index'))

    context = {"logname": logname}

    # Otherwise, render the static login page
    return flask.render_template("login.html", **context)


@MDE.app.route('/accounts/login', methods=['POST'])
def login_user():
    """Login in user and redirect them to index."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
     
    if not username or not password:
       flask.abort(400)

    # Check the login info combo
    if not validate_credentials(username, password):
       flask.abort(403)

    # If we're all good, set the session cookie
    sc_name = MDE.config.SESSION_COOKIE_NAME
    flask.session[sc_name] = username

     # Redirect to index
    return flask.redirect(flask.url_for('show_index'))


@MDE.app.route('/accounts/logout/', methods=['POST'])
def logout_user():
    """Remove session cookie and redirects to '/'"""
    flask.session.clear()

    return flask.redirect(flask.url_for('show_index'))
