from flask import Flask, jsonify, request, current_app
from json import JSONEncoder
from .views import main_views
from sqlalchemy import create_engine, text


class CustomJSONEncoder(JSONEncoder):
    """ Custom JSON encoder for testing connection with MySQL """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


def create_app(config=None):
    """ Flask application factory with blueprint(concrete views) """
    app = Flask(__name__)
    if config is None:
        app.config.from_pyfile('../config.py')
    else:
        app.config.update(config)

    database = create_engine(app.config['DB_URL'])
    app.database = database
    app.register_blueprint(main_views.bp)
    return app
