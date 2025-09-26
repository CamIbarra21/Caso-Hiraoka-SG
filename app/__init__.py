from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .routes import main_routes

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(main_routes)

    return app