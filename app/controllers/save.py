from app import app
from flask import redirect, request
from datetime import datetime
from app.models.Save import Save
from flask_login import current_user
from app.models.Feed import Feed

@app.get('/save')
def get_save():

    title = request.args.get('title')
    link = request.args.get('link')
    portalname = request.args.get('portalname')
    post_date = request.args.get('post_date')

    try:
        post_date = datetime.strptime(post_date, "%H:%M:%S %d/%m/%Y")
    except ValueError:
        return 'DATA ALTERADA'

    if title and link and portalname and post_date:

        edit_date = datetime.now()

        # Query portalname -> feed_id
        feed = Feed.get_feed_by_portalname(portalname)

        save = Save(title, link, post_date, edit_date, current_user.id, feed.id)
        save.commit_save()

        return redirect('/newsfeed')
        
    return "SAFE "