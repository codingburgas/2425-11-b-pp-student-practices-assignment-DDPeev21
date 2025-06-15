from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

# Extension instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import blueprints after extensions are initialized
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.user import user as user_blueprint
    from app.errors import errors as errors_blueprint

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(errors_blueprint)

    return app 