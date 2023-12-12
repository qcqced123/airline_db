from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, insert, delete, select, and_

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.forms import UserCreateForm, UserLoginForm, StaffLoginForm


bp = Blueprint('auth', __name__, url_prefix='/')


def generate_user_id(database: sessionmaker, userAccount: Table) -> str:
    """ Generate new UserId for new user """
    query = select(userAccount.c.UserId).order_by(userAccount.c.UserId.desc()).limit(1)
    last_user_id = database.execute(query).scalar()

    if last_user_id:
        user_id_number = int(last_user_id[1:]) + 1
        new_user_id = 'U' + str(user_id_number).zfill(5)
        return new_user_id
    else:
        return 'U00001'


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    """ Concrete view for sign-up page """
    from app import engine, metadata_obj, database
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        userAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
        user = select(userAccount.c.UserName).where(userAccount.c.UserName == form.username.data)
        result = database.execute(user).scalar()

        if result is None:
            new_user_id = generate_user_id(database, userAccount)
            newbie = insert(userAccount).values(
                UserId=new_user_id, UserName=form.username.data, UserPassword=form.password1.data
            )
            database.execute(newbie)
            database.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
            flash(result)
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    """ Concrete view for sign-in page """
    from app import engine, metadata_obj, database
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        userAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
        userid = select(userAccount.c.UserId).where(userAccount.c.UserName == form.username.data)
        username = select(userAccount.c.UserName).where(userAccount.c.UserName == form.username.data)
        user_password = select(userAccount.c.UserPassword).where(userAccount.c.UserName == form.username.data)
        uid, name, password = database.execute(userid).scalar(), database.execute(username).scalar(), database.execute(user_password).scalar()
        if name is None:
            error = "존재하지 않는 사용자입니다."
        elif not password == form.password.data:
            error = "비밀번호가 올바르지 않습니다."

        if error is None:
            """ login success case """
            session.clear()
            session['user_id'] = uid
            session['user_name'] = name
            return redirect(url_for('main.personal'))

        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/staff_login/', methods=('GET', 'POST'))
def staff_login():
    """ Concrete view for staff sign-in page """
    error = ""
    form = StaffLoginForm()
    rootName, rootPassword = 'root', '1234!'
    if request.method == 'POST' and form.validate_on_submit():
        inputName = form.staffID.data
        if rootName != inputName:
            error = "존재하지 않는 사용자입니다."
        elif rootPassword != form.password.data:
            error = "비밀번호가 올바르지 않습니다."

        if rootName == inputName and rootPassword == form.password.data:
            """ login success case """
            session.clear()
            session['user_id'] = inputName
            return redirect(url_for('main.staff'))
        flash(error)
    return render_template('./auth/staffLogin.html', form=form)
