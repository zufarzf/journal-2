from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_babelex import Babel
# from flask_moment import Moment
from flask_login import LoginManager
from flask_msearch import Search
from flask_ckeditor import CKEditor

from config import config

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
# moment = Moment()
# babel = Babel(app)
manager = LoginManager()
search = Search()
ckeditor = CKEditor()

from . import models


def create_app(config_name):
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    # moment.init_app(app)
    manager.init_app(app)
    search.init_app(app)
    ckeditor.init_app(app)

    from .main import main
    from .admin import admin_panel
    app.register_blueprint(main)
    app.register_blueprint(admin_panel)

    return app