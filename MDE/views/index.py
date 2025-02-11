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
from MDE.views.authorize import is_loggedin


@MDE.app.route('/')
def show_index():
    """Display / route.  Initializes React."""
    logname = is_loggedin()
    context = {"logname": logname}
    return flask.render_template("index.html", **context)

@MDE.app.route('/user/<username>/')
def show_user_page(username):
    """Display a user's personal page."""
    logname = is_loggedin()

    connection = MDE.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM Users "
        "WHERE username = ?",
        (username, )
    )

    user = cur.fetchone()

    # redirect user back to login page if they no longer exist
    if user is None:
        return flask.redirect('/login/')

    # get reviews
    cur = connection.execute(
        "SELECT L.country_name, L.state_name, L.city_name, L.address, L.building_name, R.review_id, R.content, R.overall, R.sidewalk_quality, R.slope, R.road_dist, R.sidewalk, R.public_trans, R.created "
        "FROM OwnsReview ORV "
        "JOIN Reviews R ON R.review_id = ORV.review_id AND ORV.user_id = ? "
        "JOIN ReviewLocation RL ON RL.review_id = R.review_id "
        "JOIN Locations L ON L.location_id = RL.location_id "
        "ORDER BY R.created DESC",
        (user['user_id'], )
    )

    reviews = cur.fetchall()

    context = {"user": user,
               "reviews": reviews,
               "num_reviews": len(reviews),
               "logname": logname}
    return flask.render_template("user.html", **context)
