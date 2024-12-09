"""Contains the add_review API function."""
import flask
import MDE
import MDE.model
from MDE.views.authorize import is_loggedin

@MDE.app.route('/api/review/add/', methods=['POST'])
def add_review():
    """Adds a review to the database"""
    # Check authorization
    logname = is_loggedin()
    if logname == "":
        flask.abort(403)

    # Check for required argument
    if 'locationid' not in flask.request.args:
        flask.abort(400)

    # Check for required data in JSON
    data = flask.request.get_json()
    if "overall" not in data:
        flask.abort(400)

    locationid = flask.request.args.get("locationid")

    connection = MDE.model.get_db()

    # Check to ensure location and user exists
    cur = connection.execute(
        "SELECT location_id "
        "From Locations "
        "WHERE location_id = ?",
        (locationid, )
    )
    loc = cur.fetchone()["location_id"]

    cur = connection.execute(
        "SELECT user_id "
        "FROM Users "
        "WHERE username = ?",
        (logname, )
    )
    userid = cur.fetchone()["user_id"]

    if loc is None or userid is None:
        flask.abort(404)

    # Add the new review to the database
    connection.execute(
        "INSERT INTO Reviews(content, overall, sidewalk_quality, slope, road_dist) "
        "VALUES (?, ?, ?, ?, ?)",
        (data.get("content"), data.get("overall"), data.get("quality"), data.get("slope"), data.get("dist"))
    )

    cur = connection.execute(
        "SELECT last_insert_rowid()",
        tuple()
    )
    reviewid = cur.fetchone()["last_insert_rowid()"]
    
    # Create mapping between user and their review
    connection.execute(
        "INSERT INTO OwnsReview "
        "(user_id, review_id) "
        "VALUES(?, ?)",
        (userid, reviewid)
    )

    # Create mapping between location and the review
    connection.execute(
        "INSERT INTO ReviewLocation(location_id, review_id) "
        "VALUES (?, ?)",
        (locationid, reviewid)
    )

    # Get the updated averages
    cur = connection.execute(
        "SELECT avg(overall), avg(sidewalk_quality), avg(slope), avg(road_dist) "
        "FROM Reviews R "
        "JOIN ReviewLocation RL "
        "ON R.review_id = RL.review_id "
        "WHERE RL.Location_id = ?",
        (locationid, )
    )
    avgs = cur.fetchone()

    # Create the context
    context = {
        "review": {
            "username": logname,
            "content": data.get("content"),
            "is_owner": True
        },
        "overall": avgs["overall"],
        "sidewalk_quality": avgs["sidewalk_quality"],
        "slope": avgs["slope"],
        "road_dist": avgs["road_dist"]
    }

    return flask.make_response(flask.jsonify(**context), 201)
