from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello():
    """ Routing Method(Concrete View) """
    return 'Hello, World!!'


@bp.route('/')
def index():
    """ Concrete view for rendering main page """
    return render_template('base.html')


@bp.route('/menu')
def personal():
    """ Concrete view for personal information page """
    return render_template('./user/menu.html')


@bp.route('/management')
def staff():
    """ Concrete view for personal information page """
    return render_template('staff/management.html')
