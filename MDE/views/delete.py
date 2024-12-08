"""Handles account deletion."""
import flask
import MDE
from MDE.views.authorize import validate_credentials

@MDE.app.route('/accounts/delete/', methods=['POST'])
def delete_account():
    """Delete a user account."""
    # Check if the user is logged in
    if 'username' not in flask.session:
        flask.abort(403)
    
    connection = MDE.model.get_db()
    
    # Delete user's reviews
    cur = connection.execute(
        "DELETE FROM Reviews "
        "WHERE user_id IN "
        "(SELECT user_id FROM Users WHERE username = ?)",
        (flask.session['username],)
    )
    
    connection.commit()
    
    # Delete user
    cur = connection.execute(
        "DELETE FROM Users "
        "WHERE username = ? ",
        (flask.session['username],)
    )
    
    connection.commit()
    
    return flask.redirect(flask.url_for('show_login'))
    