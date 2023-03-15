from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from central.settings import Config, SqlAConfig
import logging
from logging.handlers import SMTPHandler


db = SQLAlchemy(metadata=SqlAConfig.metadata)
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(config=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    
    from central.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from central.user import bp as user_bp
    app.register_blueprint(user_bp)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], \
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
    return app