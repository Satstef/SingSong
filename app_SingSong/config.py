import os
import tempfile


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'_5#y2L"F4Q8z\n\xec]/'
    UPLOAD_FOLDER = os.path.join('SingSong/static/upload_song')
    ALLOWED_EXTENSIONS = {'mp3'}
    # variabile utilizzata per scrivere il path del file nel Database
    DOWNLOAD_FILE = os.path.join('/static/upload_song')
    # Serve per evitare di mettere il next nell'url. Comunque il next funziona
    USE_SESSION_FOR_NEXT = True

class Development(Config):
    EXPLAIN_TEMPLATE_LOADING=False
    DATABASE = os.path.join(os.environ.get('DATABASE_URL'), 'DBschema/Database.db')
    DB_SCHEMA = os.path.join(os.environ.get('DB_SCHEMA_URL'), 'DBschema/schema.sql')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class Testing(Config):
    TESTING = True
    db_fd, DATABASE = tempfile.mkstemp()


class Production(Config):
    # Configurare i valori con le variabili d'ambiente. Da terminale lanciare:
    # export MAIL_SERVER = serveremail, ecc.
    DATABASE = os.path.join(os.environ.get('DATABASE_URL'), 'DBschema/Database.db')
    DB_SCHEMA = os.path.join(os.environ.get('DB_SCHEMA_URL'), 'DBschema/schema.sql')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
