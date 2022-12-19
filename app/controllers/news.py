from app import app, db
from app.models.List import List
from app.models.News import News
from app.models.List_Feed import List_Feed
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.controllers.helpers import get_xml
from flask import render_template, request
from flask_paginate import Pagination, get_page_parameter
from app.controllers.helpers import apology

PER_PAGE = 15

@app.route('/news')
@login_required
def news():

    smtm = db.select(List_Feed).join(List_Feed.list).join(List_Feed.feed).where(List.user_id == current_user.id)
    list_feed = db.session.execute(smtm).all()

    now = datetime.now()
    update_delay = timedelta(minutes=5)
    delete_delay = timedelta(hours=24)

    for item in list_feed:
        
        min_to_update = item[0].feed.update_date + update_delay
        min_to_delete = item[0].feed.update_date + delete_delay

        if now > min_to_delete:
            smtm = db.select(News).where(News.feed_id == item[0].feed.id)
            old_news = db.session.execute(smtm).all()
            for news in old_news:
                db.session.delete(news[0])

        if now > min_to_update:
            
            xml = get_xml(item[0].feed.url)
            for element in xml.find_all('item'):
                pub_date = datetime.strptime(element.pubDate.string, "%a, %d %b %Y %H:%M:%S %z")
                news = News(element.title.string, element.link.string, pub_date, item.feed.id)

                smtm = db.select(News).where(News.url == news.url)
                old_news = db.session.execute(smtm).first()

                if not old_news:
                    db.session.add(news)

        item[0].feed.update_date = now
  
    db.session.commit()

    items = []

    for feed in list_feed:
        smtm = db.select(News).join(News.feed).where(News.feed_id == feed[0].feed.id)
        news = db.session.execute(smtm).all()

        items += [(item[0], feed[0]) for item in news]


    items = sorted(items, key=lambda item: item[0].post_date, reverse=True)

    utc = timedelta(hours=-3)

    for item in items:

        item[0].post_date += utc


    length = len(items)

    search = False
    q = request.args.get('q')
    if q:
        search = True


    page = request.args.get(get_page_parameter(), type=int, default=1)

    last_page = length // PER_PAGE + 1
    if page > last_page:
        return apology('Not Found', 404)

    i = (page-1)*PER_PAGE
    items = items[i:i+PER_PAGE]
    pagination = Pagination(page=page, total=length, search=search, record_name='items', per_page=PER_PAGE)
    
    return render_template('index.html', feed=items, pagination=pagination)