"""REST API for comments."""
import flask
import insta485
from insta485.api.base import check_auth, status_codes


@insta485.app.route("/api/v1/comments/", methods=['POST'])
def add_comments():
    """Add a comment to the database."""
    # Connect to the database
    connection = insta485.model.get_db()

    # HTTP Basic Access Authentication
    logname = check_auth(connection, flask.request.authorization)
    if logname == "":
        return flask.make_response(flask.jsonify(**(status_codes[403])), 403)

    # Get data from the request
    data = flask.request.get_json()
    if 'postid' not in flask.request.args:
        return flask.make_response(flask.jsonify(**(status_codes[400])), 400)
    postid = flask.request.args['postid']
    text = data.get("text")

    # Check if the post exists
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE postid = ?",
        (postid, )
    )
    post = cur.fetchone()
    if post is None:
        return flask.make_response(flask.jsonify(**(status_codes[404])), 404)

    # Add the comment to the database
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?, ?, ?)",
        (logname, postid, text)
    )

    # Retrieve the ID of the most recently inserted comment
    cur = connection.execute("SELECT last_insert_rowid()")
    comment_id = cur.fetchone()["last_insert_rowid()"]

    # Return the new comment's ID and a 201 status code (Created)
    context = {
        "commentid": comment_id,
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl": f"/users/{logname}/",
        "text": text,
        "url": f"/api/v1/comments/{comment_id}/"
    }
    return flask.make_response(flask.jsonify(**context), 201)


@insta485.app.route("/api/v1/comments/<int:commentid>/", methods=["DELETE"])
def del_comments(commentid):
    """Delete comments from the database."""
    # Connect to database
    connection = insta485.model.get_db()

    # HTTP Basic Access Authentication
    logname = check_auth(connection, flask.request.authorization)
    if logname == "":
        return flask.make_response(flask.jsonify(**(status_codes[403])), 403)

    # Check if comment exists
    cur = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid, )
    )
    comment = cur.fetchone()
    if comment is None:
        return flask.make_response(flask.jsonify(**(status_codes[404])), 404)

    # Check that logname owns the comment
    if comment["owner"] != logname:
        return flask.make_response(flask.jsonify(**(status_codes[403])), 403)

    # Delete comment
    connection.execute(
        "DELETE FROM comments "
        "WHERE commentid = ?",
        (commentid, )
    )

    return '', 204
