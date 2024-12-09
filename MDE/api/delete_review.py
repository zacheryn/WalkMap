"""Delete the specified review from the database."""
import flask
import MDE
import MDE.model
from MDE.views.authorize import is_loggedin


@MDE.app.route('/api/review/delete/', methods=['DELETE'])
def delete_reviews():
    """Delete the specified review from the database."""
    # Check if user is logged in
    logname = is_loggedin()
    if logname == "":
        flask.abort(403)

    # Check for required arg
    if "reviewid" not in flask.request.args:
        flask.abort(400)

    reviewid = flask.request.args["reviewid"]
    connection = MDE.model.get_db()

    # Ensure logged in user owns the review
    cur = connection.execute(
        "SELECT U.user_id "
        "FROM Users U "
        "JOIN OwnsReview O "
        "ON U.user_id = O.user_id "
        "WHERE O.review_id = ?",
        (reviewid, )
    )
    result = cur.fetchone()

    if result is None:
        flask.abort(403)

    # Delete the review
    connection.execute(
        "PRAGMA foreign_keys=ON"
    )

    connection.execute(
        "DELETE FROM Reviews "
        "WHERE review_id = ?",
        (reviewid, )
    )

    context = {
        "status_code": 204,
        "message": "Success"
    }

    return flask.make_response(flask.jsonify(**context))
