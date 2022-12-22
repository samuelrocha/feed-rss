from app import app, db
from app.models.News import News
from app.models.Save import Save
from flask import redirect, render_template, request
from app.controllers.helpers import apology, PER_PAGE
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter

@app.get('/save/add/<id>')
@login_required
def add_save(id: None):
        
    if id.isnumeric():
        
        smtm = db.select(Save).where(Save.news_id == id).where(Save.user_id == current_user.id)
        save = db.session.execute(smtm).first()

        if not save:
            smtm = db.select(News).where(News.id == id)
            news = db.session.execute(smtm).first()

            if news:

                save = Save(current_user.id, id)
                db.session.add(save)
                db.session.commit()
                return redirect('/news')
            else:
                return apology("News not found", 400)
        return apology("Alredy in the saved list", 400)

@app.route('/save/list')
def list_save():

    smtm = db.select(News, Save).join(Save.news).join(News.feed).where(Save.user_id == current_user.id)
    news = db.session.execute(smtm).all()

    length = len(news)

    search = False
    q = request.args.get('q')
    if q:
        search = True


    page = request.args.get(get_page_parameter(), type=int, default=1)

    last_page = length // PER_PAGE + 1
    if page > last_page:
        return apology('Not Found', 404)

    i = (page-1)*PER_PAGE
    news = news[i:i+PER_PAGE]
    pagination = Pagination(page=page, total=length, search=search, record_name='news', per_page=PER_PAGE)

    return render_template('save_list.html', news=news, pagination=pagination)

@app.route("/save/remove/<id>")
def remove_save(id: None):

    if id.isnumeric():

        smtm =  db.select(Save).where(Save.news_id == id).where(Save.user_id == current_user.id)
        news = db.session.execute(smtm).first()

        if news:
            db.session.delete(news[0])
            db.session.commit()

        return redirect('/save/list')
    
    return apology('???', 400)