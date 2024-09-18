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
