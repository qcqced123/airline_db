from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify
from werkzeug.utils import redirect
from sqlalchemy import create_engine, text

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello():
    """ Routing Method(Concrete View) """
    return 'Hello, World!!'


@bp.route('/')
def index():
    """ Concrete view for rendering main page """
    return render_template('base.html')
