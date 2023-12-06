from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify
from sqlalchemy import create_engine, text

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello():
    """ Routing Method(Concrete View) """
    return 'Hello, World'
