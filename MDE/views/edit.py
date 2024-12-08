"""Handles account editing."""
import flask
import MDE
from MDE.views.authorize import validate_credentials

@MDE.app.route('/edit/')
def show_edit():
    """Display /edit/ route."""
    # Check if user is logged in, if not, redirect to login
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
        
    # If logged in, grab all of their current account data to populate the fields with
    connection = MDE.model.get_db()
    
    cur = connection.execute(
        "SELECT * "
        "FROM Users "
        "WHERE username = ?",
        (flask.session['username'],)
    )
    
    user = cur.fetchone()

    # Render the account edit page
    return flask.render_template(
        "edit.html", {"user": user}
    )

@MDE.app.route('/accounts/edit/', methods=['POST'])
def edit_account(){
    """Create a new user account."""
    # Check if the user is logged in
    if 'username' not in flask.session:
        flask.abort(403)
            
    # Start by getting and checking input
    firstname = flask.request.form.get('firstname')
    lastname = flask.request.form.get('lastname')
    username = flask.request.form.get('username')
    new_password1 = flask.request.form.get('newpassword1')
    new_password2 = flask.request.form.get('newpassword2')
    password = flask.request.form.get('password')
    email = flask.request.form.get('email')
    file = flask.request.files['file']

    if not password:
        flask.abort(400)
        
    # Handle simple updates first
    query = "UPDATE Users SET"
    parameters = []
    
    connection = MDE.model.get_db()
    
    if firstname:
        query += " first_name = ?,"
        parameters.append(firstname)
    if lastname:
        query += " last_name = ?,"
        parameters.append(lastname)
    if username:
        # Check that new username does not exists
        cur = connection.execute(
            "SELECT COUNT(*) as count "
            "FROM Users "
            "WHERE username = ?",
            (username,)
        )
        
        result = cur.fetchone()
        
        if result['count'] > 0:
            flask.abort(409)
        
        query += " username = ?,"
        parameters.append(username)
    if email:
        query += " email = ?,"
        parameters.append(email)
    
    if query != "UPDATE Users SET":
        query = query[0:len(query) - 1]
        
        query += " WHERE username = ?"
        parameters.append(flask.session['username'])
        
        connection.execute(query, tuple(parameters])
        connection.commit()
    
    # Handle new profile picture
    if file:
        # Get the name of the old file
        cur = connection.execute(
            "SELECT filename "
            "FROM Users "
            "WHERE username = ?",
            (flask.session['username'],)
        )
        query = cur.fetchone()
        old = MDE.app.config["UPLOAD_FOLDER"]/query['filename']
        
        # Remove it
        old.unlink()

        # Calculate and save the new filename
        suffix = pathlib.Path(file.filename).suffix.lower()
        stem = uuid.uuid4().hex
        uuid_basename = f"{stem}{suffix}"
        path = MDE.app.config["UPLOAD_FOLDER"]/uuid_basename
        file.save(path)

        # Update the filename
        connection.execute(
            "UPDATE Users "
            "SET filename = ? "
            "WHERE username = ?",
            (uuid_basename, flask.session['username'])
        )
        connection.commit()
        
    # Handle new password
    if new_password1 and new_password2:
        # Verify the current password
        if not check_password(flask.session['username'], password):
            flask.abort(403)

        # Verify that new passwords match
        if not new_password1 == new_password2:
            flask.abort(401)

        # Hash the new password
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + new_password1
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Update the password
        connection.execute(
            "UPDATE Users "
            "SET password = ? "
            "WHERE username = ?",
            (password_db_string, flask.session['username'])
        )
        connection.commit()
    
    # Redirect back to edit so user can see new changes
    return flask.redirect(flask.url_for(show_edit))
}