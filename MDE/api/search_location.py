"""REST API for location search."""
import flask
import MDE


@MDE.app.route('/api/location/find/', methods=['GET'])
def search_location():
    """Searches for a location in the database given country, state, city, address, building"""
    # Create error response if needed
    error_response = {
        "message": "Not Found",
        "status_code": 404
    }

    connection = MDE.model.get_db()
    cur = None

    # If no query parameters provided, fetch a random location
    if len(flask.request.args) == 0:
        cur = connection.execute(
            "SELECT latitude, longitude "
            "FROM Locations "
            "ORDER BY random() LIMIT 1"
        )
    else:
        query = "SELECT latitude, longitude FROM Locations WHERE "
        parameter_list = []
        is_first = True

        # Attempt to extract any search parameters for the query's where clause
        try:
            if 'country' in flask.request.args:
                parameter_list.append(str(flask.request.args['country']))
                if is_first == False:
                    query += "AND "
                else:
                    is_first = False
                query += "country_name = ? "
            if 'state' in flask.request.args:
                parameter_list.append(str(flask.request.args['state']))
                if is_first == False:
                    query += "AND "
                else:
                    is_first = False
                query += "state_name = ? "
            if 'city' in flask.request.args:
                parameter_list.append(str(flask.request.args['city']))
                if is_first == False:
                    query += "AND "
                else:
                    is_first = False
                query += "city_name = ? "
            if 'address' in flask.request.args:
                parameter_list.append(str(flask.request.args['address']))
                if is_first == False:
                    query += "AND "
                else:
                    is_first = False
                query += "address = ? "
            if 'building' in flask.request.args:
                parameter_list.append(str(flask.request.args['building']))
                if is_first == False:
                    query += "AND "
                else:
                    is_first = False
                query += "building_name = ? "
        except:
            # If string conversion of any parameters fails, return a 400 Bad Request
            error_response["message"] = "Bad Request"
            error_response["status_code"] = 400

            return flask.make_response(flask.jsonify(**error_response), 400)

        query += "limit 1"

        if len(parameter_list) == 0:
            cur = connection.execute(
                "SELECT latitude, longitude "
                "FROM Locations "
                "ORDER BY random() LIMIT 1"
            )
        else:
            cur = connection.execute(
                query,
                tuple(parameter_list)
            )

    location = cur.fetchone()

    # If no location was found that matches, return a 404 Not Found
    if location is None:
        return flask.make_response(flask.jsonify(**error_response), 404)

    context = {
        "longitude": location["longitude"],
        "latitude": location["latitude"]
    }

    return flask.make_response(flask.jsonify(**context), 201)
