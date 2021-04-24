import sqlite3
from sqlite3 import Error
from flask import (Flask, render_template, request, flash, redirect, url_for,
    current_app)
from flask_login import current_user, login_user, login_required, logout_user
import os
from . import auth
from .forms import RegistraForm, LoginForm
from .db_conn import insert_utente, login_ok, load_user, User, delete_user_notconfirmed
from werkzeug.security import generate_password_hash
from SingSong.email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# ----------------- RICEVERE I DATI UTENTE DA FORM REGISTRAZIONE -------------------------
#indicare il file del template in cui si trova il form
@auth.route('/registra', methods=['POST', 'GET'])
def registra():
    # se lo user è già loggato, gli impediamo di tornare sulla pagina di login
    if current_user.is_authenticated:
        return redirect(url_for('profile.user_can', nome=current_user.nome))
    form = RegistraForm()
    if form.validate_on_submit():
        hash_pss = generate_password_hash(form.password.data, "pbkdf2:sha256")
        # creo la lista dei valori inseriti nei campi dall'utente. Questi sono i
        # 4 valori da inserire nel DB
        user_data= list(form.data.values())[0:3]
        # sostituisco la password nella lista con l'hash
        user_data[2] = hash_pss
        insert_utente(user_data)
        mes_ins = "Data entered correctly"
        mes_log = "A confirmation email has been sent to you by email"

        """L'utente è stato inserito nel DB, ma ancora non si può loggare; la FUNZIONE
        send_email gli invierà una mail con link per confermare la registrazione.
        Il link di conferma contiene un token generato con itsdangerous.
        La generazione del token utilizza la funzione generate_confirmation_token,
        istanza dell'oggeto User (in db_conn). Quindi il token è saldamente legato all'id utente.
        La funzione load_user, in db_conn, restituisce esattamente l'oggetto User"""
        email = form.email.data
        id = login_ok(email)
        user = load_user(id)
        nome = user.nome
        # utilizzo l'oggetto User per creare e legare il token all'id.
        token = user.generate_confirmation_token()
        # Invio email con token di conferma per confermare
        subject = "User account confirmation!"
        send_email(email, subject, "email_confirm", nome=nome, token=token)
        # Chiamo la funzione da db.conn che cancella l'utente se non ha confermato
        # entro lo scadere del token. In questo modo può registrarsi di nuovo.
        delete_user_notconfirmed(id)
        return render_template('reg_index.html', form=form, mi=mes_ins, ml=mes_log)
    return render_template('reg_index.html', form=form)


# ------------------------- PAGINA DI LOGIN  --------------------------------
# Ricevo i dati da login
@auth.route("/login", methods=['POST', 'GET'])
def login():
    # se lo user è già loggato, gli impediamo di tornare sulla pagina di login
    if current_user.is_authenticated:
        return redirect(url_for('profile.user_can', nome=current_user.nome))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        """Il processo del login funziona così: recupero l'id dell'utente che si sta loggando
        e lo passo alla funzione load_user (in db_conn). Ritorna l'oggetto User (che
        contiene user id, Nome, email e password cioè contiene tutta la riga dei dati relativi
        all'utente). L'oggetto poi può essere passato alla funzione login_user per il login. """
        id = login_ok(email)
        Us = load_user(id)
        """ login_user è il momento in cui l'utente viene loggato e le classi
        is_active e is_authenticated risultano True.
        parametro:remember se True, ad ogni login, viene lasciato nel browser un cookie
        'remember_token' che permette di riaccedere al proprio profilo anche chiudendo
        il browser. Bisogna però andare diretti al proprio profilo, altrimenti il cookie
        verrà cancellato."""
        # se l'utente non ha confermato il link non può entrare.
        if Us.conferma == False:
            flash('You must confirm your account first. Please check your email!')
            return render_template('log_in.html', form=form)
        login_user(Us, remember=form.remember_me.data)
        return redirect(url_for('profile.user_can', nome=current_user.nome))
    return render_template('log_in.html', form=form)



@auth.route("/confirm/<token>", methods=['GET', 'POST'])
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    # Con try vogliamo testare se il link è scaduto o non valido. In quest'ultimo
    # caso restituisce errore e chiede di registrarsi di nuovo se l'utente non è già confermato.
    try:
        # .loads() decodifica il token appena ricevuto tramite email;
        # il token diventa un dizionario {confirm:self.id}
        data = s.loads(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'invalid')
        flash("""If you did not confirm your account trough email and can't login,
            please register again.""", 'invalid')
        return redirect(url_for('main.home'))
    # prendo email dal token
    email = data.get('email')
    id = login_ok(email)
    user = load_user(id)
    # Se il campo Conferma del DB è True,quindi utente già predentemente confermato.
    if user.conferma:
        logout_user()
        flash('Your account is already confirmed, you can login!', 'confirm')
        return redirect(url_for('main.home'))
    # Se l'utente ha appena confermato via mail viene richiamata la funzione confirm_email
    # da db_conn per validare il token.
    if user.confirm_email(data):
        nome = user.nome
        # Viene creata la cartella personale per i files delle canzoni
        os.mkdir("SingSong/static/upload_song/" + nome)
        flash('You have confirmed your account, thanks! You can login now.', 'confirm')
        return redirect(url_for('main.home'))
    else:
        # In tutti gli altri casi la conferma non avviene.
        flash('The confirmation link is invalid or has expired. Please register again.',
            'invalid')
        return redirect(url_for('main.home'))
