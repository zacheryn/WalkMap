"""Services dealing with authentication."""
import hashlib
import uuid
import flask
import MDE

def is_loggedin():
    """Validate that the user has a valid login"""
    
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    
    if 'username' not in flask.session or 'password' not in flask.session:
            return False
    
    authorized = validate_credentials(username, password)
    
    if not authorized:
        return False
    
    return True

def validate_credentials(username, password):
    """Validate username and password."""
    # Connect to the database and get the salt and correct hash
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM Users "
        "WHERE username = ?",
        (username,)
    )
    result = cur.fetchone()
    if result is None:
        return False
    algorithm, salt, correct_hash = result['password'].split('$')

    # Hash the plain text input password
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    attempt_hash = hash_obj.hexdigest()

    # Check that the password is correct
    return attempt_hash == correct_hash
