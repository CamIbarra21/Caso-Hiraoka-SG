from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import Cliente
    return Cliente.query.get(int(user_id))