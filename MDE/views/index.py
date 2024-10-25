"""
MDE index view.

URLs include:
/
/user/<username>
"""
import uuid
import pathlib
import hashlib
import flask
import arrow
import MDE


@MDE.app.route('/')
def show_index():
    """Display / route.  Initializes React."""

    # For compilation purposes
    context = {}
    return flask.render_template("index.html", **context)

@MDE.app.route('/user/<username>/')
def show_user_page(username):
    """Display a user's personal page."""

    connection = MDE.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM Users "
        "WHERE username = ?",
        (username, )
    )

    user = cur.fetchone()

    # TODO: redirect user back to login page if they no longer exist
    user_exists = user is None

    # get reviews
    cur = connection.execute(
        "SELECT L.address, R.review_id, R.content, R.overall, R.sidewalk_quality, R.slope, R.road_dist, R.sidewalk, R.public_trans, R.created "
        "FROM OwnsReview ORV "
        "JOIN Reviews R ON R.review_id = ORV.review_id AND ORV.user_id = ? "
	"JOIN ReviewLocation RL ON RL.review_id = R.review_id"
	"JOIN Locations L ON L.location_id = RL.location_id"
        "ORDER BY R.created DESC",
        (user['user_id'], )
    )

    reviews = cur.fetchall()

    context = {"user": user, "reviews": reviews, "num_reviews": len(reviews)}
    return flask.render_template("user.html", **context)

