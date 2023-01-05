from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, manager
from app.main.UserLogin import UserLogin
from app.main.forms import LoginForm
from app.models import *


@manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route('/')
def index():
    person = Personal.query.all()
    lenth = len(person)

    # create unique admin
    def add_admin():
        user = Personal(login='jouradmin', psw=generate_password_hash('health123312'), is_admin=True)

        db.session.add(user)
        db.session.commit()

    if lenth == 0:
        add_admin()

    count = 0
    for i in person:
        if i.login == 'jouradmin' and check_password_hash('health123312', i.psw):
            count += 1
        else:
            continue

    if count != 0:
        add_admin()
    # ======== ========= =========

    informations = Email.query.first()
    info_cat = VolumeCat.query.filter_by(current=True).first()

    editional = []
    special = []
    simple = []

    url = request.base_url

    if info_cat:
        info_vol = VolumeInfo.query.filter_by(vol_cat=info_cat.id).all()

        for i in info_vol:
            if i.editional:
                editional.append(i)
            elif i.special:
                special.append(i)
            else:
                simple.append(i)

    return render_template('main-index.html', info=informations,
                           info_cat=info_cat, url=url,
                           editional=editional, special=special,
                           simple=simple)

@app.route('/about')
def aboutjour():
    informations = Email.query.first()
    return render_template('about-1.html', info = informations)


@app.route('/aim-scope')
def aim():
    informations = Email.query.first()
    return render_template('about-2.html', info = informations)


@app.route('/editionalTeam')
def team():
    informations = Email.query.first()
    return render_template('about-3.html', info = informations)


@app.route('/editorial-policy')
def policy():
    informations = Email.query.first()
    return render_template('about-4.html', info = informations)


@app.route('/submission')
def submission():
    informations = Email.query.first()
    return render_template('submission.html', info = informations)


# ======= the dynamic part of the website =======
@app.route('/current')
def current():
    informations = Email.query.first()

    informations = Email.query.first()
    info_cat = VolumeCat.query.filter_by(current=True).first()

    editional = []
    special = []
    simple = []

    if info_cat:
        info_vol = VolumeInfo.query.filter_by(vol_cat=info_cat.id).all()

        for i in info_vol:
            if i.editional:
                editional.append(i)
            elif i.special:
                special.append(i)
            else:
                simple.append(i)

    url = request.base_url

    return render_template('articles-1.html', info=informations,
                           info_cat=info_cat, url=url,
                           editional=editional, special=special,
                           simple=simple)

@app.route('/archive')
def archive():
    informations = Email.query.first()
    categories = VolumeCat.query.all()

    return render_template('article-2.html', info = informations, cat=categories)


@app.route("/archive/<path:volume>")
def volume(volume):
    informations = Email.query.first()

    info_cat = VolumeCat.query.filter_by(name=volume).first()

    editional = []
    special = []
    simple = []

    if info_cat:
        info_vol = VolumeInfo.query.filter_by(vol_cat=info_cat.id).all()

        for i in info_vol:
            if i.editional:
                editional.append(i)
            elif i.special:
                special.append(i)
            else:
                simple.append(i)

    url = request.base_url

    return render_template('volume.html', info=informations,
                           info_cat=info_cat, url=url,
                           editional=editional, special=special,
                           simple=simple)


@app.route('/just-accepted')
def just():
    informations = Email.query.first()

    info_cat = VolumeCat.query.filter_by(just=True).first()

    editional = []
    special = []
    simple = []

    if info_cat:
        info_vol = VolumeInfo.query.filter_by(vol_cat=info_cat.id).all()


        for i in info_vol:
            if i.editional:
                editional.append(i)
            elif i.special:
                special.append(i)
            else:
                simple.append(i)

    url = request.base_url

    return render_template('article-3.html', info=informations,
                           info_cat=info_cat, url=url,
                           editional=editional, special=special,
                           simple=simple)


# @app.route('/search/<path:item>', methods=['POST', 'GET'])
# def search(item):
#     informations = Email.query.first()
#
#     return render_template('search.html', info = informations,item=item)
#

@app.route('/search/')
def search():
    informations = Email.query.first()

    cat_items = []
    items = []
    item = request.args.get('query')
    if item:
        items = VolumeInfo.query.msearch(item, fields=['text', 'author'])
        cat_items = VolumeCat.query.msearch(item, fields=['name'])
    else:
        items = []

    return render_template('search.html', info=informations, items=items, cat_items=cat_items)


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if current_user.get_id():
        idp = current_user.get_id()
        us = Personal.query.filter_by(id=idp).first()
        if current_user.is_authenticated and us.is_admin:
            return redirect(url_for('admin.index'))


    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        psw = form.psw.data

        users = Personal.query.all()

        for user in users:
            pas = check_password_hash(user.psw, psw)
            user_per = Personal.query.filter_by(login=name).first()
            if user.login == name and pas:
                userlogin = UserLogin().create(user_per)
                # rm = True if request.form.get('remember') else False
                # print(rm)
                login_user(userlogin)

                return redirect(url_for('admin.index'))


    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))