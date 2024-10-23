"""Contains the retrieve_locations API  function."""
import flask
import MDE
import MDE.model


@MDE.app.route('/api/location/list/', methods=['GET'])
def retrieve_locations():
    """Returns a list of all locations within a range of coordinates."""
    # Check that all needed args are present
    if 'latmin' not in flask.request.args \
       or 'latmax' not in flask.request.args \
       or 'longmin' not in flask.request.args \
       or 'longmax' not in flask.request.args:
        error_msg = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.make_response(flask.jsonify(**error_msg), 400)

    # Connect to the database
    connection = MDE.model.get_db()

    # Query the server using a parameterized statement
    cur = connection.execute(
        "SELECT location_id, country_name, state_name, city_name, "
        "address, building_name, longitude, latitude "
        "FROM Locations "
        "WHERE longitude > ? "
        "AND longitude < ? "
        "AND latitude > ? "
        "AND latitude < ?",
        (float(flask.request.args.get('longmin')), float(flask.request.args.get('longmax')),
         float(flask.request.args.get('latmin')), float(flask.request.args.get('latmax')))
    )

    # Take the results of the query and put them into a LIST
    locations = cur.fetchall()
    print(locations)

    # take the results and put them into a context DICT
    context = {
        "locations": locations
    }

    # Return the context as a JSON with a 201 SUCCESS status code
    return flask.make_response(flask.jsonify(**context), 201)
