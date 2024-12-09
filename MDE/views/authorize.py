"""Services dealing with authentication."""
import hashlib
import uuid
import flask
import MDE
import MDE.model

def is_loggedin() -> str:
    """Validate that the user has a valid login"""
    logname = ""

    # Check if authorization header is used
    if flask.request.authorization is None \
       or "username" not in flask.request.authorization \
       or "password" not in flask.request.authorization:
        # Look for a session cookie
        sc_name = MDE.app.config['SESSION_COOKIE_NAME']
        if sc_name in flask.session:
            logname = flask.session[sc_name]

            # Check to make sure session cookie represents a real user
            connection = MDE.model.get_db()
            cur = connection.execute(
                "SELECT user_id "
                "FROM Users "
                "WHERE username = ?",
                (logname, )
            )
            user_id = cur.fetchone()
            if user_id is None:
                flask.session.clear()
                return ""
        else:
            return ""
    else:
        logname = flask.request.authorization['username']
        password = flask.request.authorization['password']
    
        authorized = validate_credentials(logname, password)
    
        if not authorized:
            return ""
    
    return logname

def validate_credentials(username, password) -> bool:
    """Validate username and password."""
    # Connect to the database and get the salt and correct hash
    connection = MDE.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM Users "
        "WHERE username = ?",
        (username,)
    )
    result = cur.fetchone()
    if result is None:
        print("result")
        return False
    algorithm, salt, correct_hash = result['password'].split('$')

    # Hash the plain text input password
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    attempt_hash = hash_obj.hexdigest()

    print(attempt_hash)
    print(correct_hash)
    # Check that the password is correct
    return attempt_hash == correct_hash
