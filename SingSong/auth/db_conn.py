import sqlite3
from wtforms.validators import ValidationError
from werkzeug.local import LocalProxy
from SingSong.Database import get_db, close_db
from SingSong import login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import threading


""" Questo file contiene le funzioni relative ai validatori e tutte le funzioni
che inseriscono o richiamano dati."""


"""********       FUNZIONI PER I VALIDATORI FORM REGISTRA       *******"""

# Recupero della lista dei nomi
def nome_list():
     conn = get_db()
     cur = conn.cursor()
     cur.execute('SELECT Nome FROM Dati_utente')
     tup_lis = cur.fetchall()
     close_db(e=None)
     return tup_lis

# Recupero della lista delle email
def email_list():
     conn = get_db()
     cur = conn.cursor()
     cur.execute('SELECT Email FROM Dati_utente')
     tup_lis = cur.fetchall()
     close_db(e=None)
     return tup_lis


"""********       FUNZIONI PER I VALIDATORI FORM LOGIN       *******"""

"""Viene richiamata dal DB la password (in formato hash) in corrispondenza della
riga contenente la mail inserita dall'utente in fase di login.
IMPORTANTE: se la mail inserita dall'utente in fase di login non esiste nel DB,
hash_pass avrà un valore nullo, è necessario che venga chiamato un errore di validazione.
In caso contrario l'hash viene ottenuto come tupla, quindi trasformato in lista e
ritorna come semplice stringa
parametro:email la mail inserita dall'utente in fase di login."""
def password_call(email):
    conn = get_db()
    cur = conn.cursor()
    hash_pass = cur.execute("""SELECT Password FROM Dati_utente
        WHERE Email=?""", [email]).fetchone()
    close_db(e=None)
    if hash_pass is None:
        raise ValidationError('Wrong password')
    hash_pass = list(hash_pass)
    return hash_pass[0]



"""********        DATI CONFERMATI DA REGISTRA E LOGIN       *******
                        esportare in views """

"""Funzione di inserimento dati dell'utente nel DB
parametro:dati lista di nome, email e password_has dell'utente"""
def insert_utente(dati):
    sql = "INSERT INTO Dati_utente (Nome, Email, Password) VALUES (?,?,?)"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, dati)
    conn.commit()
    close_db(e=None)
    return

"""Una volta che i dati di login sono stati validati e confermati, la Funzione
recuera il nome in corrispondenza della mail inserita. Il nome verrà restituito
nella pagina del profilo utente"""
def login_ok(email):
    conn = get_db()
    cur = conn.cursor()
    id = cur.execute('SELECT Utente_id FROM Dati_utente WHERE Email=?', [email]).fetchone()
    id = list(id)
    close_db(e=None)
    return id[0]



"""********        OGGETTO E FUNZIONE load_user PER FLASK_LOGIN      *******"""

"""Creo un oggetto della tabella Dati_Utente del DB. Questo oggetto "User" serve
per la funzione login_user in views. Grazie a questa classe posso richiamare i dati
id, nome ecc semplicemente con current_user.id o current_user.nome"""
class User(UserMixin):
    def __init__(self, id, nome, email, password, conferma):
        self.id = id
        self.nome = nome
        self.email = email
        self.password = password
        self.conferma = conferma

    def is_active(self):
         return True

    def is_anonymous(self):
         return False

    def is_authenticated(self):
         return True

    def is_active(self):
         return True

    def get_id(self):
         return self.id

    """TOKEN DI CONFERMA VIA EMAIL
    L'oggetto TimedJSONWebSignatureSerializer (importato come Serializer) fornisce due metodi:
    dumps() crea una signature crittografata ed expires_in indica i secondi di validità della signature.
    load() decodifica la signature."""
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # dumps codifica il dizionario {confirm:self.id} in un token.
        # Il token è quindi collegato all'id utente appena registrato
        return s.dumps({'confirm': self.id, 'email': self.email})

    # Funzione utilizzata nella route di conferma del token; verifica se il TOKEN
    # ricevuto via mail, dopo essere decodificato (loads(token)), corrisponde
    # al valore del dizionario "self.id", decodificato precedentemente.
    def confirm_email(self, data):
        # Se il valore (self.id) del dizionario (richiamato tramite la chiave 'confirm')
        # non corrisponde al valore self.id (l'id reale dell'utente registrato),
        # restituisce falso, altrimenti aggiorna i campi del DB e conferma l'utente.
        if data.get('confirm') != self.id:
            return False
        conn = get_db()
        cur = conn.cursor()
        values = [True, self.id]
        cur.execute("""UPDATE Dati_utente SET Conferma = ? WHERE Utente_id=?""", values)
        values[0]=datetime.datetime.now()
        cur.execute("""UPDATE Dati_utente SET Confermato_il = ? WHERE Utente_id=?""", values)
        conn.commit()
        close_db(e=None)
        return True



"""Questa funzione viene richiamata da login_user in views. Dato un id
utente, viene utilizzata per richiamare dal DB i dati di un utente e assegnarli all'oggetto User (sopra).
Cioè, partendo dall'id, restituisce un oggetto che rappresenta un utente con i valori
espressi in return(us_data[0], us_data[1]) che corrispondono a id, nome ecc dell'oggetto User (sopra).
Questo oogetto (che rappresenta lo user) e dato dal "modello del DB", serve per implementare 4 metodi
nella classe User (is_active, is_authenticated, ecc). Inoltre serve per implementare metodi quali:
current_user, logout_user, login_required.
La funzione è implementata per DB ORM tipo SQLAlchemy, ma qui è stata riadattata per
SQLite3 (vedi https://medium.com/analytics-vidhya/how-to-use-flask-login-with-sqlite3-9891b3248324)"""
@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Dati_utente WHERE Utente_id=?', [user_id])
    us_data = cur.fetchone()
    return User(int(us_data[0]), us_data[1], us_data[2], us_data[3], bool(us_data[4]))



"""********        CANCELLA UTENTE SE NON CONFERMA TOKEN      *******"""

"""Queste funzioni cancellano l'utente se non conferma il suo account entro lo scadere del token
impostato a 1 ora. La prima funzione innesca un timer che si avvia allo scadere del token.
Il threading.Timer richiama la funzione delete_user la quale creare un nuovo oggetto
"user", e controlla se l'utente ha confermato il suo account. Se il campo "conferma"
restituisce false, l'utente non ha confermato e viene cancellato. Essendo un nuovo
thread è necessario definire app_context."""
def delete_user_notconfirmed(id):
    app = current_app._get_current_object()
    threading.Timer(3800.0, delete_user, args=[app, id]).start()
    return

def delete_user(app, id):
    with app.app_context():
        user = load_user(id)
        conn = get_db()
        cur = conn.cursor()
        id = user.id
        if user.conferma:
            return
        else:
            cur.execute("DELETE FROM Dati_utente WHERE Utente_id=?", [id])
            conn.commit()
            close_db(e=None)
            return
