from .db_conn import trac_list, list_song
from wtforms.validators import ValidationError
from flask_login import current_user
import os
from os import listdir
from os.path import isfile, join
from config import Config
import re


"""********        VALIDATORI CANZONE      *******"""

"""Come prima cosa recupera dal DB le canzoni dell'utente connesso
che vengono restituite in forma di lista.
I due validatori controllano se la traccia è già presente nel DB, associata o all'Album
inserito dall'utente o all'artista o a entrambi.
In tutti questi casi solleva un errore."""
def traccia_check(form, field):
    traccia = form.titolo.data
    album = form.album.data
    artista = field.data
    nome = current_user.nome
    if traccia in trac_list(nome):
        lista = list_song(traccia)
        if traccia in lista and album in lista and artista in lista:
            raise ValidationError("""The song title already exists and is associated with
                the album and artist you entered. Please use update form to moodify songs. """)
        if traccia in lista and artista in lista:
            raise ValidationError("""The song title already exists and is associated with
                the artist you entered. Please use update form to moodify songs.""")

"""Validatore per album field"""
def traccia_check_alb(form, field):
    traccia = form.titolo.data
    artista = form.artista.data
    album = field.data
    nome = current_user.nome
    if traccia in trac_list(nome):
        lista = list_song(traccia)
        if traccia in lista and album in lista and artista not in lista or artista == "":
            raise ValidationError("""The song title already exists and is associated with
                the album you entered. Please use update form to moodify songs """)



"""********        VALIDATORE FILE CARICATO      *******"""

"""Controlla che il file inserito non sia già presente nella cartella personale.
Il nome originale del file viene modificato dal metodo secure_file()
per essere messo in sicurezza e poi viene depositato nel DB.
È necessario quindi prevedere come secure_file trasformerà il nome file e
confrontarlo con i files presenti nella cartella personale per vedere se già presente
Tra le cose che fa il metodo: elimina gli spazi bianchi ssotituendoli con un
underscore; elimina gli undersocre all' inizio del file. Le seguenti linee di codice cerc"""
def filename_match(form, field):
    nome = current_user.nome
    # Creo la lista delle canzoni presenti nella cartella.
    file_list = [f for f in listdir(os.path.join(Config.UPLOAD_FOLDER, nome))
        if isfile(join(os.path.join(Config.UPLOAD_FOLDER, nome), f))]
    # Le seguenti 8 linee di codice prevedono come secure_file trasformerà il nome file.
    # Il nuovo nome ottenuto viene poi confrontato con quelli già presenti nella cartella canzoni.
    file = form.file.data.filename
    new_list = file.split()
    string = ""
    for word in new_list:
        string += word + "_"
    str = slice(0, len(string)-1)
    new_string = (string[str])
    new_string = re.sub('^_+',"", new_string)
    # Confronto la lista delle canzoni con quella inserita dall'utente.
    if new_string in file_list:
        raise ValidationError("""The file already exists.""")
