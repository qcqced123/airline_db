from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify
from sqlalchemy import Table
from sqlalchemy import insert, delete, select

from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from app.forms import UserCreateForm
# from app.models import AddUser


bp = Blueprint('auth', __name__, url_prefix='/')


# @bp.route('/signup', methods=('GET', 'POST'))
# def signup():
#     from app import db, engine, metadata_obj, database
#     form = UserCreateForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         user = AddUser.query.filter_by(username=form.username.data).first()
#         if not user:
#             user = AddUser(
#                 username=form.username.data,
#                 password=generate_password_hash(form.password1.data),
#             )
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('main.index'))
#         else:
#             flash('이미 존재하는 사용자입니다.')
#     return render_template('auth/signup.html', form=form)

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    from app import db, engine, metadata_obj, database
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        userAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
        user = select(userAccount.c.UserName).where(userAccount.c.UserName == form.username.data)
        result = database.execute(user).scalar()
        if result is not None:
            newbie = insert(userAccount).values(
                UserId='U0071', UserName=form.username.data, UserPassword=form.password1.data
            )  # insert
            database.execute(newbie)
            database.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

