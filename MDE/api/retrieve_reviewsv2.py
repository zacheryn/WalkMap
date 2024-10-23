import json
import flask
import MDE

@MDE.app.route('/api/review/list/', methods=['GET'])
def search_location():

    error_response = {
        "message": "Bad Request",
        "status_code": 400
    }
    
    #connect to the database
    connection = MDE.model.get_db()

    #return 400 bad request error if location id not provided...not sure how to check if malformed
    if 'locationid' not in flask.request.args:
        return flask.make_response(flask.jsonify(**error_response), 400)
    
    #get location id
    try: 
        id = int(flask.request.args['locationid'])
    except:
        return flask.make_response(flask.jsonify(**error_response), 400)

    #fetch review ids by location id
    cur = connection.execute(
        "SELECT review_id"
        "FROM ReviewLocation"
        "WHERE location_id=?",
        (id)
    )
    
    review_ids = cur.fetchall()
    
    #create a parameterized query for the in clause
    parameters = ', '.join('?' for _ in review_ids)

    #fetch reviews by review id
    cur = connection.execute(
        f"SELECT R.review_id, R.content, R.overall, R.sidewalk_quality, R.slope, R.road_dist, R.sidewalk, R.public_trans, U.first_name, U.last_name "
        "FROM Reviews R"
        "JOIN OwnsReview ORV ON ORV.review_id = R.review_id"
        "JOIN Users U ON U.user_id = ORV.user_id"
        "WHERE review_id in ({parameters})",
        (review_ids)
    )
    
    reviews = cur.fetchall()
    
    owners_and_reviews = cur.fetchall()

    context = {
        "reviews" : reviews
    }
    
    return flask.make_response(flask.jsonify(**context), 201)





