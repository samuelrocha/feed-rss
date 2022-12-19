from app import app, db
from app.models.Feed import Feed
from app.models.List import List
from app.models.News import News
from app.models.List_Feed import List_Feed
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.controllers.helpers import get_xml
from flask import render_template

@app.route('/news')
@login_required
def news():

    smtm = db.select(Feed, List).join(List_Feed.list).join(List_Feed.feed).where(List.user_id == current_user.id)
    feeds = db.session.execute(smtm).all()
    
    now = datetime.now()
    update_delay = timedelta(minutes=5)
    delete_delay = timedelta(hours=24)

    for feed in feeds:
        min_to_update = feed[0].update_date + update_delay
        min_to_delete = feed[0].update_date + delete_delay

        if now > min_to_delete:
            smtm = db.select(News).where(News.feed_id == feed[0].id)
            old_news = db.session.execute(smtm).all()
            for item in old_news:
                db.session.delete(item[0])

        if now > min_to_update:
            
            xml = get_xml(feed[0].url)
            for item in xml.find_all('item'):
                pub_date = datetime.strptime(item.pubDate.string, "%a, %d %b %Y %H:%M:%S %z")
                news = News(item.title.string, item.link.string, pub_date, feed[0].id)

                smtm = db.select(News).where(News.url == news.url)
                old_news = db.session.execute(smtm).first()

                if not old_news:
                    db.session.add(news)

        feed[0].update_date = now
    
    db.session.commit()

    items = []
    for feed in feeds:
        smtm = db.select(News).join(News.feed).where(News.feed_id == feed[0].id)
        news = db.session.execute(smtm).all()

        items += [(item[0], feed[1]) for item in news]


    items = sorted(items, key=lambda item: item[0].post_date, reverse=True)

    utc = timedelta(hours=-3)

    for item in items:

        item[0].post_date += utc
    return render_template('index.html', feed=items)