import json
import flask
import MDE

@MDE.app.route('/api/review/list/')
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
    id = flask.request.args['locationid']

    #fetch review ids by location id
    cur = connection.execute(
        "SELECT review_id"
        "FROM ReviewLocation"
        "WHERE location_id=id"
    )
    review_ids = cur.fetchall()

    #fetch reviews by review id
    cur = connection.execute(
        "SELECT review_id, content, overall, sidewalk_quality, slope, road_dist, sidewalk, public_trans "
        "FROM Reviews"
        "WHERE review_id in review_ids"
    )
    reviews = cur.fetchall()

    #also fetch owners...
    cur = connection.execute(
        "SELECT *"
        "FROM OwnsReview"
        "WHERE review_id in review_ids"
    )
    owners_and_reviews = cur.fetchall()

    #now for each id in review_ids, match the associated owner_id from owners_and_reviews to the 
    #associated review from reviews
    returnlist = []
    for x in review_ids:
        #search owners table for owner name by id
        this_owner = [b[0] for a,b in enumerate(owners_and_reviews) if b[1] == x]
        cur = connection.execute(
            "SELECT first_name, last_name"
            "FROM Users"
            "WHERE user_id = this_owner"
        )
        owner_name = cur.fetchone() #should just be one anyway
        this_review = [(b[1],b[2],b[3],b[4],b[5],b[6],b[7]) for a,b in enumerate(reviews) if b[0] == x] #this can't be the right/the easiest way...
        returnlist.append((owner_name, this_review))

    context = {
        "reviews" : returnlist
    }
    return flask.make_response(flask.jsonify(**context), 201)





