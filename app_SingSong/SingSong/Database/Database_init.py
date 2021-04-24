import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


"""Connessione al DB utilizzando g. g is a special object that is unique for each request.
It is used to store data that might be accessed by multiple functions during the request.
The connection is stored and reused instead of creating a new connection if get_db is
called a second time in the same request."""
def get_db():
    if 'db' not in g:
        # connessione utilizzando current_app (va a guardare dentro la cartella
        # dell'app; config richiama la variabile del file config.py)
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db


"""Chiusura della connessione al DB"""
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


"""********       INIZIALIZZAZIONE DEL DATABASE       *******"""

"""Creazione del DB utente seguendo lo schema."""
def create_database():
    # Connessione al file del Database
    conn = get_db()
    # Richiamo il file shema.sql per creare le tabelle del DB. La variabile DB_SCHEMA
    # viene restituita da config.py come stringa.
    schema_path = current_app.config['DB_SCHEMA']
    with current_app.open_resource(schema_path) as f:
        # eseguo la lettura del file schema.sql
        conn.executescript(f.read().decode('utf-8'))
    return conn

"""Creazione della linea di comando per creare un nuovo database."""
# Creazione del comando init-db per avviare il DB
@click.command('init-db')
@with_appcontext
def create_database_command():
    create_database()
    click.echo('Database creato con successo')

"""Questa funzione deve essere importata in __init__.py generale (factory)
e essere avviata richiamandola"""
def init_db(app):
    app.cli.add_command(create_database_command)
