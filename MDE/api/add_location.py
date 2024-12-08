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
    
    # Check that all needed args are present
    lat = flask.request.args['lat']
    long = flask.request.args['long']
    country = flask.request.args['country']
    state = flask.request.args['state']
    city = flask.request.args['city']
    
    parameters = [lat, long, country, state, city]
    
    if not all(parameters):
        flask.abort(400)
    
    # Connect to the database
    connection = MDE.model.get_db()
    
    query = ("INSERT INTO Locations "
             "(latitude, longitude, country_name, state_name, city_name")
    
    if 'address' in flask.request.args:
        query += ", address"
        parameters.append(flask.request.args['address'])
    if 'building' in flask.request.args:
        query += ", building"
        parameters.append(flask.request.args['building'])
    
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
    
    if address:
        context['address'] = address
    if building:
        context['building'] = building
    
    return flask.make_response(flask.jsonify(**context), 201)