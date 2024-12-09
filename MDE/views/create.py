"""Handles account creation."""
import flask
import MDE
import pathlib
import uuid
import hashlib
import MDE.config
from MDE.views.authorize import is_loggedin

@MDE.app.route('/create/')
def show_create():
    """Display /create/ route."""
    # Redirect to /accounts/edit/ if the user is logged in
    logname = is_loggedin()
    if logname != "":
        return flask.redirect(flask.url_for('show_edit'))

    # Render the account creation page
    context = {"logname": logname}
    return flask.render_template("create.html", **context)

@MDE.app.route('/accounts/create/', methods=['POST'])
def create_account():
    """Create a new user account."""
    # Start by getting and checking input
    firstname = flask.request.form.get('firstname')
    lastname = flask.request.form.get('lastname')
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    email = flask.request.form.get('email')
    file = flask.request.files['file']

    if not all([firstname, lastname, username, password, email]):
        flask.abort(400)

    # Check if the user already exists
    connection = MDE.model.get_db()
    
    cur = connection.execute(
        "SELECT COUNT(*) as count "
        "FROM Users "
        "WHERE username = ?",
        (username,)
    )
    
    result = cur.fetchone()
    if result['count'] > 0:
        flask.abort(409)

    # Save the profile picture file
    if file is not None:
        suffix = pathlib.Path(file.filename).suffix.lower()
        uuid_basename = f"{uuid.uuid4().hex}{suffix}"
        path = MDE.app.config["UPLOAD_FOLDER"]/uuid_basename
        file.save(path)

    # Hash the password
    hash_obj = hashlib.new('sha512')
    password_salted = uuid.uuid4().hex + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join([
        'sha512',
        uuid.uuid4().hex,
        hash_obj.hexdigest()
    ])
    
    # Create the account
    if file is None:
        connection.execute(
            "INSERT INTO Users "
            "(username, first_name, last_name, email, password) "
            "VALUES "
            "(?, ?, ?, ?, ?)",
            (username, firstname, lastname, email, password_db_string)
        )
    else:
        connection.execute(
            "INSERT INTO Users "
            "(username, first_name, last_name, email, filename, password) "
            "VALUES "
            "(?, ?, ?, ?, ?, ?)",
            (username, firstname, lastname, email, uuid_basename, password_db_string)
        )
    connection.commit()
    
    # Set cookie
    flask.session[MDE.config.SESSION_COOKIE_NAME] = username
    
    # Redirect to index
    return flask.redirect(flask.url_for('show_index'))