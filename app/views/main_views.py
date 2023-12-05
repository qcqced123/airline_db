from flask import Blueprint, render_template


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello_pybo():
    """ Routing Method(Concrete View) """
    return 'Hello, Pybo!!!!!'
