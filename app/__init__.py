import config

from flask import Flask, jsonify, request, current_app
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import insert, delete


db = SQLAlchemy()
migrate = Migrate()
engine, metadata_obj, database = None, None, None


class CustomJSONEncoder(JSONEncoder):
    """ Custom JSON encoder for testing connection with MySQL """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


def create_app(test_config=None):
    from .views import main_views, auth_views, price_views
    """ Flask application factory with blueprint(concrete views) """
    global engine, metadata_obj, database
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(config)
    else:
        app.config.update(test_config)

    # make connection with MySQL DB
    app.json_encoder = CustomJSONEncoder
    engine = create_engine(app.config['DB_URL'], echo=True)
    metadata_obj = MetaData()
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    database = sessionLocal()

    # Apply Concrete Views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(price_views.bp)
    database.close()

    return app
