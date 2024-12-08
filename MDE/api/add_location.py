"""Contains the add_location API function."""
import flask
import MDE
from MDE.views.authorize import is_loggedin

@MDE.app.route('/api/location/add/', methods=['POST'])
def add_location():
    """Adds a location to the database"""
    # Check authorization
    if not is_loggedin():
        flask.abort(403)
    
    # Check for required args
    if 'lat' not in flask.request.args \
       or 'long' not in flask.request.args \
       or 'country' not in flask.request.args \
       or 'state' not in flask.request.args \
       or 'city' not in flask.request.args:
           flask.abort(400)
    
    query = ("INSERT INTO Locations "
             "(latitude, longitude, country_name, state_name, city_name")
    
    parameters = [lat, long, country, state, city]
           
    # Check that all args are of required format
    try:
        lat = float(flask.request.args['lat'])
        long = float(flask.request.args['long'])
        country = str(flask.request.args['country'])
        state = str(flask.request.args['state'])
        city = str(flask.request.args['city'])
        
        if 'address' in flask.request.args:
            query += ", address"
            address = str(flask.request.args['address'])
            parameters.append(address)
        if 'building' in flask.request.args:
            query += ", building"
            building = str(flask.request.args['building'])
            parameters.append(building)
    except:
         # If conversion of any parameters fails, return a 400 Bad Request
        flask.abort(400)
    
    # Connect to the database
    connection = MDE.model.get_db()
    
    query += ")"
    
    question_marks = "?, " * len(parameters)
    question_marks = question_marks[0:len(question_marks) - 2]
    
    query += f" VALUES ({question_marks}) "
    
    connection.execute(query, tuple(parameters))
    connection.commit()
    
    cur = connection.execute(
        "select last_insert_rowid() "
    )
    
    locationid = cur.fetchone()
    
    context = {
        "locationid": locationid,
        "lat": lat,
        "long": long,
        "country": country,
        "state": state,
        "city": city
    }
    
    if 'address' in flask.request.args:
        context['address'] = address
    if 'building' in flask.request.args:
        context['building'] = building
    
    return flask.make_response(flask.jsonify(**context), 201)