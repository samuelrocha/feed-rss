from app import app, db
from app.models.forms import AddListForm, EditListForm
from app.models.List import List
from app.models.List_Feed import List_Feed
from app.controllers.helpers import apology, PER_PAGE
from flask import request, render_template, redirect
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter


@app.route("/list/add", methods=['GET', 'POST'])
@login_required
def add_list():

    form = AddListForm()

    if request.method == "POST":

        if form.validate_on_submit():

            name = form.name.data
            smtm = db.select(List).where(
                List.user_id == current_user.id).where(List.name == name)
            listr = db.session.execute(smtm).first()

            if not listr:

                listr = List(name, current_user.id)
                db.session.add(listr)
                db.session.commit()

                return redirect('/list')

            return "LISTA JÁ EXISTE"

        return "FORMULARIO INCORRETO"

    return render_template('list_add.html', form=form)


@app.route("/list")
@login_required
def show_list():

    smtm = db.select(List).where(
        List.user_id == current_user.id).where(List.name != 'General')
    lists = db.session.execute(smtm).all()

    length = len(lists)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    last_page = length // PER_PAGE + 1
    if page > last_page:
        return apology('Not Found', 404)

    i = (page-1)*PER_PAGE
    lists = lists[i:i+PER_PAGE]
    pagination = Pagination(
        page=page, total=length, search=search, record_name='lists', per_page=PER_PAGE)

    return render_template('list_show.html', lists=lists, pagination=pagination)


@app.route('/list/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_list(id=None):

    form = EditListForm()

    smtm = db.select(List).where(List.id == id).where(
        List.user_id == current_user.id).where(List.name != 'General')
    listr = db.session.execute(smtm).first()

    if listr:

        if request.method == 'POST':
            if form.validate_on_submit():

                smtm = db.select(List).where(List.user_id == current_user.id).where(
                    List.name == form.name.data)
                other_list = db.session.execute(smtm).first()

                if not other_list:
                    listr[0].name = form.name.data
                    db.session.commit()
                    return redirect('/list')
                return "list alredy exist"
            return 'form incorrect'

        form.id.data = id
        form.name.data = listr[0].name
        return render_template("list_edit.html", form=form)

    return apology('page not found', 404)

@app.route('/list/remove/<id>')
@login_required
def remove_list(id=None):

    smtm = db.select(List).where(List.id == id).where(List.user_id == current_user.id)
    listr = db.session.execute(smtm).first()

    if listr:
        smtm = db.select(List_Feed).where(List_Feed.list_id == listr[0].id)
        list_feed = db.session.execute(smtm).all()

        if list_feed:
            for item in list_feed[0]:
                db.session.delete(item)
        db.session.delete(listr[0])
        db.session.commit()
        return redirect('/list')

    return apology('page not found', 404)