"""MDE package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (MDE/config.py)
app.config.from_object('MDE.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable MDE_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export MDE_SETTINGS=secret_key_config.py
app.config.from_envvar('MDE_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import MDE.api  # noqa: E402  pylint: disable=wrong-import-position
import MDE.views  # noqa: E402  pylint: disable=wrong-import-position
import MDE.model  # noqa: E402  pylint: disable=wrong-import-position
