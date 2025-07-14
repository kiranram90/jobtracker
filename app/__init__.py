from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from app.extensions import db, migrate, login_manager


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost/jobtracker')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    from app.models.users import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)



    # Import and register blueprints here
    from app.controllers.auth_controller import auth_bp 
    from app.controllers.application_controller import application_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(auth_bp)

    return app