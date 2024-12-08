"""Contains the add_review API function."""
import flask
import MDE
from MDE.views.authorize import is_loggedin

@MDE.app.route('/api/review/add/', methods=['POST'])
def add_review():
    """Adds a review to the database"""
    # Check authorization
    if not is_loggedin():
        flask.abort(403)
    
    if 'overall' not in flask.request.args:
        flask.abort(400)
    
    parameters = []
    
    query = ("INSERT INTO Reviews "
             "(overall")
             
    context = {}
    
    # Attempt to extract all parameters as their correct types
    try:
        overall = float(flask.request.args['overall'])
        parameters.append(overall)
        context['overall'] = overall
        
        if 'content' in flask.request.args['content']:
            content = str(flask.request.args['content'])
            query += ", content"
            parameters.append(content)
            context['content'] = content
            
        if 'quality' in flask.request.args['quality']:
            quality = int(flask.request.args['quality'])
            query += ", quality"
            parameters.append(quality)
            context['quality'] = quality
        
        if 'slope' in flask.request.args['slope']:
            slope = int(flask.request.args['slope'])
            query += ", slope"
            parameters.append(slope)
            context['slope'] = slope
            
        if 'dist' in flask.request.args['dist']:
            dist = int(flask.request.args['dist'])
            query += ", dist"
            parameters.append(dist)
            context['dist'] = dist
            
        if 'sidewalk' in flask.request.args['sidewalk']:
            sidewalk = bool(flask.request.args['sidewalk'])
            query += ", sidewalk"
            parameters.append(sidewalk)
            context['sidewalk'] = sidewalk
            
        if 'pubtrans' in flask.request.args['pubtrans']:
            pubtrans = bool(flask.request.args['pubtrans'])
            query += ", pubtrans"
            parameters.append(pubtrans)
            context['pubtrans'] = pubtrans
    except:
        # If string conversion of any parameters fails, return a 400 Bad Request
        flask.abort(400)
    
    # Connect to the database
    connection = MDE.model.get_db()
    
    query += ")"
    
    question_marks = "?, " * len(parameters)
    question_marks = question_marks[0:len(question_marks) - 2]
    
    query += f" VALUES ({question_marks})"
    
    # Insert the review
    connection.execute(query, tuple(parameters))
    connection.commit()
    
    cur = connection.execute(
        "select last_insert_rowid() "
    )
    
    reviewid = cur.fetchone()
    
    # Grab its created on date
    cur = connection.execute(
        "SELECT created "
        "FROM Reviews "
        "WHERE review_id = ?",
        (reviewid,)
    )
    
    createdon = cur.fetchone()
    
    # Grab the logged in user's id
    cur = connection.execute(
        "SELECT user_id, username "
        "FROM Users "
        "WHERE username = ?",
        (flask.session['username'],)
    )
    
    user = cur.fetchone()
    
    # Create mapping between user and their review
    cur = connection.execute(
        "INSERT INTO OwnsReview "
        "(user_id, review_id) "
        "VALUES(?, ?)",
        (userid, reviewid, )
    )
    
    context['reviewid'] = reviewid
    context['userid'] = user['user_id']
    context['username'] = user['username']
    context['created'] = createdon['created']
    
    return flask.make_response(flask.jsonify(**context), 201)