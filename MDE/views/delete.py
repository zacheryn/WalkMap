"""Handles account deletion."""
import flask
import MDE
import MDE.model
from MDE.views.authorize import is_loggedin, validate_credentials

@MDE.app.route('/accounts/delete/', methods=['POST'])
def delete_account():
    """Delete a user account."""
    # Check if the user is logged in
    logname = is_loggedin()
    if logname == "" or logname != flask.request.form.get("logname"):
        print("Death")
        print(f"{logname}, {flask.request.form}")
        flask.abort(403)

    if "password" not in flask.request.form:
        flask.abort(403)

    validate_credentials(logname, flask.request.form["password"])

    connection = MDE.model.get_db()

    # Delete user's reviews
    connection.execute(
        "PRAGMA foreign_keys=ON"
    )

    connection.execute(
        "DELETE FROM Reviews "
        "WHERE Reviews.review_id IN "
        "(SELECT O.review_id "
        "FROM OwnsReview O "
        "JOIN Users U "
        "ON O.user_id = U.user_id "
        "WHERE U.username = ?)",
        (logname,)
    )

    # Delete user
    connection.execute(
        "DELETE FROM Users "
        "WHERE username = ? ",
        (logname,)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_login'))
