"""REST API for location search."""
import json
import flask
import MDE

@MDE.app.route('/api/location/find/', methods=['GET'])
def search_location():
	"""Searches for a location in the database given country, state, city, address, building"""
	
	# TODO: add authentication checking
	
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
                "select * from Locations ",
                "order by random() limit 1"
	    )
	else
	    query_where_clause = "where "
	    parameter_list = []
            is_first = true
	    
            # Attempt to extract any search parameters for the query's where clause
            try:
		if 'country' in flask.request.args:
		    parameter_list.append(str(flask.request.args['country']))
                    if is_first == False:
                        query_where_clause += "and "
                    else:
                        is_first = False
		    query_where_clause += "country_name = ? "
                if 'state' in flask.request.args:
		    parameter_list.append(str(flask.request.args['state']))
                    if is_first == False:
                        query_where_clause += "and "
                    else:
                        is_first = False
		    query_where_clause += "state_name = ? "
                if 'city' in flask.request.args:
		    parameter_list.append(str(flask.request.args['city']))
                    if is_first == False:
                        query_where_clause += "and "
                    else:
                        is_first = False
                    query_where_clause += "city_name = ? "
                if 'address' in flask.request.args:
		    parameter_list.append(str(flask.request.args['address']))
                    if is_first == False:
                        query_where_clause += "and "
                    else:
                        is_first = False
                    query_where_clause += "address = ? "
                if 'building' in flask.request.args:
		    parameter_list.append(str(flask.request.args['building']))
                    if is_first == False:
                        query_where_clause += "and "
                    else:
                        is_first = False
                    query_where_clause += "building_name = ? "
            except:
                # If string conversion of any parameters fails, return a 400 Bad Request
                error_response["message"] = "Bad Request"
                error_response["status_code"] = 400

                return flask.make_response(flask.jsonify(**error_response), 400)

             cur = connection.execute(
                "select * from Locations ",
                query_where_clause,
                "order by location_id",
                tuple(parameter_list)
	    )
		
	location = cur.fetchone()
	
        # If no location was found that matches, return a 404 Not Found
	if location is None:
		return flask.make_response(flask.jsonify(**error_response), 404)
        
        context = {
            "location" : location
        }
        
        return flask.make_response(flask.jsonify(**context), 201)
