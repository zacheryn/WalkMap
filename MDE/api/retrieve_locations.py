import flask
import MDE


@MDE.app.route('/api/location/list/', methods=['GET'])
def retrieve_locations():
    """Returns a list of all locations within a range of coordinates."""
    