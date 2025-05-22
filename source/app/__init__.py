from flask import Flask
from .extensions import db, login_manager, bootstrap, csrf, migrate, mail
from .blueprints.auth.routes import auth_bp
from .blueprints.classifier.routes import classifier_bp
from .blueprints.dashboard.routes import dashboard_bp
from app.blueprints.classifier.routes import classifier_bp
app.register_blueprint(classifier_bp)
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')


    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(classifier_bp)
    app.register_blueprint(dashboard_bp)

    return app
