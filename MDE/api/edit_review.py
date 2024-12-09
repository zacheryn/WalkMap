import flask
import MDE
from MDE.views.authorize import is_loggedin

@MDE.app.route('/api/review/edit/', methods=['POST'])
def edit_review():
    # Check authorization
    if not is_loggedin():
        flask.abort(403)
    
    if 'overall' not in flask.request.args:
        flask.abort(400)
    
    parameters = []

    review_id_in = float(flask.request.args['review_id'])
    connection = MDE.model.get_db()
    
    try:
        if 'content' in flask.request.args['content']:
            content = str(flask.request.args['content'])
            cur = connection.execute("UPDATE Reviews"
                    "Set content=(content)"
                    "where review_id=(review_id)",
                    (content, review_id_in, )
            )

        if 'quality' in flask.request.args['quality']:
            quality = int(flask.request.args['quality'])
            cur = connection.execute("UPDATE Reviews"
                    "Set quality=(quality)"
                    "where review_id=(review_id)",
                    (quality, review_id_in, )
            )
        
        if 'slope' in flask.request.args['slope']:
            slope = int(flask.request.args['slope'])
            cur = connection.execute("UPDATE Reviews"
                    "Set slope=(slope)"
                    "where review_id=(review_id)",
                    (slope, review_id_in, )
            )
        
        if 'dist' in flask.request.args['dist']:
            dist = int(flask.request.args['dist'])
            cur = connection.execute("UPDATE Reviews"
                    "Set dist=(dist)"
                    "where review_id=(review_id)",
                    (dist, review_id_in, )
            )

        if 'sidewalk' in flask.request.args['sidewalk']:
            sidewalk = bool(flask.request.args['sidewalk'])
            cur = connection.execute("UPDATE Reviews"
                    "Set sidewalk=(sidewalk)"
                    "where review_id=(review_id)",
                    (sidewalk, review_id_in, )
            )
        
        if 'pubtrans' in flask.request.args['pubtrans']:
            pubtrans = bool(flask.request.args['pubtrans'])
            cur = connection.execute("UPDATE Reviews"
                    "Set pubtrans=(pubtrans)"
                    "where review_id=(review_id)",
                    (pubtrans, review_id_in, )
            )
    except:
        flask.abort(400)

    connection.commit()
             
    return