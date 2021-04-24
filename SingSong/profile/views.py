import sqlite3
import os
from sqlite3 import Error
from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, current_user, logout_user, confirm_login
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename
import json
from config import Config
from . import prof
from .db_conn import (trac_list, list_song, insert_trac, lista_canzoni_utente,
    delete_song, update_titolo, update_alb_id, update_gen, delete_not_util)
from .forms import CanzoneForm, AggiornaCanzone


# ------------------------- PAGINA PROFILO UTENTE  --------------------------------

"""NOTA BENE: se si disattiva login_required e si inserisce l'url del profilo
manualmente, si potrebbe ricevere un errore di url non trovato in qualsiasi momento,
perchè non è stato attivato l'oggetto dato da load_user() (richiamato da login_user()).
L'oggetto per mette di attivare i metodi current_user ecc."""
@prof.route("/profile/<nome>", methods=['POST', 'GET'])
@login_required
def user_can(nome):
    form_up = AggiornaCanzone()
    form = CanzoneForm()
    if form.validate_on_submit():
        artista = form.artista.data
        album = form.album.data
        genere = form.genere.data
        traccia = form.titolo.data
        file= request.files['file']
        # Mettiamo in sicurezza il file caricato dall'utente
        filename = secure_filename(file.filename)
        # Sono state create cartelle personalizzate alla registrazione dell'utente.
        # Ora quindi viene salvato il file caricato, nel path della cartella personale.
        file.save(os.path.join(Config.UPLOAD_FOLDER, nome, filename))
        """Indico il path del file per salvarlo nel DB.
        Nota che: DOWNLOAD_FILE non è la cartella di upload (UPLOAD_FOLDER),
        ma è un path utile per poi permettere di richiamare il file sul player html.
        Inoltre bisogna usare filename per registrare il path corretto sul DB,
        perchè il secure_filename modifica il nome originale del file.
        Quindi se qui in basso si usa file.filename (al posto di filename), il nome del file
        registrato nel path del Db sarà diverso dal nome del file nella cartella
        UPLOAD_FOLDER"""
        #filepath=Config.DOWNLOAD_FILE + "/" + filename
        filepath=os.path.join(Config.DOWNLOAD_FILE, nome, filename)
        insert_trac(artista, album, genere, traccia, filepath)
        flash("Song entered correctly")
        # Necessario reindirizzo all'url per fare refresh della pagina, altrimenti
        # il form riappare con i dati compilati.
        return redirect(url_for('profile.user_can', nome=nome))
    # Funzione che rinfresca la sessione aperta come nuova.
    # Quindi il cookie remember me (remember_token) non viene distrutto. Dopo la chiusura
    # e riapertura browser, accedendo alla pagina profilo, il cookie mantiene la sessione aperta
    confirm_login()
    lista = lista_canzoni_utente(nome)
    return render_template('in_fo.html', form=form, lista=lista, form_up=form_up)

"""La funzione di logout deve essere linkata nell'html, con un url_for, alla
funzione logout qui sotto."""
@prof.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""La route a cui rimanda l'icona cancella canzone dall'html. Questa funzione
cancella il nome traccia dal DB e il file dalla cartella personale dell'utente."""
@prof.route("/profile/delete")
def del_song():
    # Ricevo l'id della canzone tramite richiesta GET dal click dell'
    # icona del cancella canzone.
    song_id = request.args.get('n')
    # Cancello il titolo della canzone dal DB, che deve corrisponde all'id canzone e
    # all'id utente
    nome = current_user.nome
    path = delete_song(song_id, nome)
    #Cancello il file dalla cartella personale
    path= "SingSong" + path
    os.remove(path)
    # Dopo aver cancellato il titolo e il file, rimuovo dal DB, album artisti e genere non collegati
    # ad alcuna traccia. In questo modo tengo pulito il DB.
    delete_not_util()
    return redirect(url_for('profile.user_can', nome=current_user.nome))


"""Quando l'utente aggiorna i dati di una canzone le funzioni di aggiornamento si trovano qui"""
@prof.route("/profile/<nome>/update", methods=['POST', 'GET'])
@login_required
def update_song(nome):
    form_up = AggiornaCanzone()
    if form_up.validate_on_submit():
        # I dati canzone aggiornati dall'utente
        artista = form_up.artista.data
        album = form_up.album.data
        genere = form_up.genere.data
        traccia = form_up.titolo.data
        traccia_id = form_up.tit_id.data

        # I dati canzone prima dell'aggiornamento. Vengono inseriti nel form automaticamente
        # quando l'utente clicca la matita. Sono inseriti in campi nascosti che l'utente non
        # può modificare.
        album_hide = form_up.alb_hide.data
        artista_hide = form_up.art_hide.data
        genere_hide = form_up.gen_hide.data
        # Modifico titolo canzone
        update_titolo(traccia_id, traccia)
        # Se sono stati modificati artista o album (rispetto ai vecchi album e artista,
        # album_hide e artista_hide), uso la funzione "update_alb_id per modificarli in DB
        if artista != artista_hide or album != album_hide:
            update_alb_id(album, artista, traccia_id)
        # MOdifico genere se modifato dall'utente.
        if genere != genere_hide:
            update_gen(genere, traccia_id)
        # rimuovo dal DB, album artisti e genere non collegati ad alcuna traccia.
        # In questo modo tengo pulito il DB!
        delete_not_util()

    return redirect(url_for('profile.user_can', nome=nome))
