"""REST API for base."""
import hashlib
import flask
import insta485


status_codes = {
    400: {
            "message": "Bad Request",
            "status_code": 400
    },
    403: {
            "message": "Forbidden",
            "status_code": 403
    },
    404: {
            "message": "Not Found",
            "status_code": 404
    }
}


def check_auth(connection, auth):
    """Check if the connection is authorized."""
    # Returns logname if authorized
    # HTTP Basic Access Authentication
    logname = ""
    if auth is None \
       or "username" not in auth \
       or "password" not in auth:
        # Check if session cookie exists
        sc_name = insta485.app.config['SESSION_COOKIE_NAME']
        if sc_name in flask.session:
            # if exists, set logname
            logname = flask.session[sc_name]
        else:
            # else, no session or http auth
            return ""
    else:
        # if http auth, check logname/passw
        logname = auth["username"]
        password = auth["password"]
        # cur = connection.execute(
        #     "SELECT password "
        #     "FROM users "
        #     "WHERE username = ?",
        #     (logname, )
        # )
        pass_hash = insta485.model.get_user_passw(connection, logname)
        if pass_hash is None:
            return ""

        # pieces = pass_hash["password"].rsplit('$')
        # hash_obj = hashlib.new(pieces[0])
        # salted_password = pieces[1] + password
        # hash_obj.update(salted_password.encode('utf-8'))
        password_hash, pieces = insta485.model.do_hashing_things(
            pass_hash, hashlib, password)
        if pieces[2] != password_hash:
            return ""
    return logname


@insta485.app.route('/api/v1/')
def return_base():
    """Return urls to other api's.

    Example:
    {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    """
    # Create context
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": flask.request.path
    }

    return flask.jsonify(**context)
