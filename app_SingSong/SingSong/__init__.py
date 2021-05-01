import os
from flask import Flask
from flask_login.login_manager import LoginManager
from config import Config, Development, Production, Testing #importo Class Config
from flask_mail import Mail


"""Settaggio di flask_login. login_manager.login_view indica il redirect nel caso un utente
cerchi di entrare in una pagina protetta da login_required."""
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access'
mail = Mail()

def create_app(config_class=Development):
    app = Flask('SingSong')
    # Dichiaro di voler attivare la configurazione Development
    app.config.from_object(config_class)
    # Inizializzazione di flask_login
    login_manager.init_app(app)
    # Inizializzazione di flask_mail
    mail.init_app(app)

    from SingSong.Database import init_db
    init_db(app)

    from SingSong.main import main as main_bp
    app.register_blueprint(main_bp)

    from SingSong.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from SingSong.profile import prof as prof_bp
    app.register_blueprint(prof_bp)

    return app
