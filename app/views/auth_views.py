from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy import Table, insert, delete, select, and_

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.forms import UserCreateForm, UserLoginForm


bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    """ Concrete view for sign-up page """
    from app import engine, metadata_obj, database
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        userAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
        user = select(userAccount.c.UserName).where(userAccount.c.UserName == form.username.data)
        result = str(database.execute(user).scalar())
        if result is None:
            newbie = insert(userAccount).values(
                UserId='U0071', UserName=form.username.data, UserPassword=form.password1.data
            )
            database.execute(newbie)
            database.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    """ Concrete view for sign-in page """
    from app import engine, metadata_obj, database
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        userAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
        username = select(userAccount.c.UserName).where(userAccount.c.UserName == form.username.data)
        user_password = select(userAccount.c.UserPassword).where(userAccount.c.UserName == form.username.data)
        name, password = database.execute(username).scalar(), database.execute(user_password).scalar()
        if name is None:
            error = "존재하지 않는 사용자입니다."
        elif not password == form.password.data:
            error = "비밀번호가 올바르지 않습니다."

        if error is None:
            """ login success case """
            session.clear()
            session['user_id'] = name
            return redirect(url_for('main.personal'))

        flash(error)
    return render_template('auth/login.html', form=form)
