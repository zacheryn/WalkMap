"""Contains the retrieve_reviews API function."""
import flask
import MDE
import MDE.config
from MDE.views.authorize import is_loggedin


@MDE.app.route('/api/review/list/', methods=['GET'])
def retrieve_reviews():
    """Return reviews for location with the given id."""

    error_response = {
        "message": "Bad Request",
        "status_code": 400
    }

    # Connect to the database
    connection = MDE.model.get_db()

    # Add loging check here
    logname = is_loggedin()

    # Return 400 bad request error if location id not provided...not sure how to check if malformed
    if 'locationid' not in flask.request.args:
        return flask.make_response(flask.jsonify(**error_response), 400)

    # Get location id
    id = flask.request.args['locationid']

    # Fetch reviews and relevant information
    cur = connection.execute(
        "SELECT Reviews.review_id, Reviews.content, Reviews.overall, "
        "Reviews.sidewalk_quality, Reviews.slope, Reviews.road_dist, "
        "Reviews.sidewalk, Reviews.public_trans, Users.username, Users.filename "
        "FROM ReviewLocation "
        "INNER JOIN Reviews "
        "ON ReviewLocation.review_id = Reviews.review_id "
        "INNER JOIN OwnsReview "
        "ON ReviewLocation.review_id = OwnsReview.review_id "
        "INNER JOIN Users "
        "ON OwnsReview.user_id = Users.user_id "
        "WHERE ReviewLocation.location_id = ?",
        (id, )
    )
    reviews = cur.fetchall()

    # Get Averages
    overall_tot = 0.0
    quality_tot = 0.0
    slope_tot = 0.0
    dist_tot = 0.0
    count = 0
    quality_count = 0
    slope_count = 0
    dist_count = 0
    for review in reviews:
        overall_tot += review["overall"]
        count += 1
        if review.get("sidewalk_quality") is not None:
            quality_tot += review["sidewalk_quality"]
            quality_count += 1
        if review.get("slope") is not None:
            slope_tot += review["slope"]
            slope_count += 1
        if review.get("road_dist") is not None:
            dist_tot += review["road_dist"]
            dist_count += 1
        if review["username"] == logname:
            review["is_owner"] = True
        else:
            review["is_owner"] = False

    # Do division in try except to account for when no reviews are present
    try:
        overall_avg = overall_tot / count
    except:
        overall_avg = 0
    try:
        quality_avg = quality_tot / quality_count
    except:
        quality_avg = 0
    try:
        slope_avg = slope_tot / slope_count
    except:
        slope_avg = 0
    try:
        dist_avg = dist_tot / dist_count
    except:
        dist_avg = 0

    context = {
        "overall": overall_avg,
        "sidewalk_quality": quality_avg,
        "slope": slope_avg,
        "road_dist": dist_avg,
        "reviews": reviews
    }

    return flask.make_response(flask.jsonify(**context), 201)
