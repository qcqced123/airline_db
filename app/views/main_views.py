from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify
from sqlalchemy import create_engine, text

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello():
    """ Routing Method(Concrete View) """
    return 'Hello, World'


# def get_user(user_id):
#     """ Get user information from database """
#     user = current_app.database.execute(text(
#         "SELECT UserId, UserName, UserPassword FROM users WHERE UserId = : user_id "
#     ), {
#         'UserId': user_id
#     }).fetchone()
#
#     return {
#         'UserId': user['UserId'],
#         'UserName': user['UserName'],
#         'UserPassword': user['UserPassword'],
#     } if user else None
#
#
# def insert_user(user):
#     """ Insert user information into current database """
#     return current_app.database.execute(text(
#         "INSERT INTO users(UserName, hashed_password) VALUES (:UserName, :UserPassword)"), user).lastrowid
#
#
# @bp.route('/sign-up', methods=['POST'])
# def sign_up():
#     """ Add new member information to db """
#     new_user = request.json
#     new_user_id = insert_user(new_user)
#     new_user = get_user(new_user_id)
#
#     return jsonify(new_user)
#
