from flask import Flask
from config import config
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.cors import CORS
import mimetypes

mimetypes.add_type("application/vnd.ms-fontobject", ".eot")
mimetypes.add_type("application/x-font-woff", ".woff")
mimetypes.add_type("font/woff2", ".woff")
mimetypes.add_type("application/x-font-ttf", ".ttf")
mimetypes.add_type("application/x-font-ttc", ".ttc")
mimetypes.add_type("font-snft", ".otf")

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from app.admin import admin as admin_blueprint
    from app.auth import auth as auth_blueprint
    from app.api import api as api_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
