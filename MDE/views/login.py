"""
Handles user login.
"""
import uuid
import pathlib
import flask
import insta485
from MDE.views.authorize import validate_credentials

@MDE.app.route('/login/')
def show_login():
    """Display /login/ route."""
    # Redirect to / if the user is logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    # Otherwise, render the static login page
    return flask.render_template(
        "login.html", {}
    )

@insta485.app.route('/accounts/login', methods=['POST'])
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
     flask.session['username'] = username

     # Redirect to index
     return flask.redirect(flask.url_for(show_index))