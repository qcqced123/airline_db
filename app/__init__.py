import config

from flask import Flask, jsonify, request, current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, delete
from .views import main_views


db = SQLAlchemy()
migrate = Migrate()


class CustomJSONEncoder(JSONEncoder):
    """ Custom JSON encoder for testing connection with MySQL """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


def create_app(test_config=None):
    """ Flask application factory with blueprint(concrete views) """
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
    db = sessionLocal()
    UserAccount = Table("UserAccount", metadata_obj, autoload_with=engine)
    test = insert(UserAccount).values(UserId='U0071', UserName='LEE', UserPassword='1234')
    db.execute(test)
    db.commit()
    db.close()

    # app.database = database
    # db.init_app(app)
    # migrate.init_app(app, db)

    app.register_blueprint(main_views.bp)
    # app.register_blueprint(auth_views.bp)

    return app
