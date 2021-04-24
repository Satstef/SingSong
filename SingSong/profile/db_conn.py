from SingSong.Database import get_db, close_db
import sqlite3
from flask_login import current_user

"""********      QUERY LISTE DELLE TABELLE DATABASE     *******"""

""" Ottengo l'id di un valore. Trasformo la tupla in lista """
def id_value(message, value, cur):
    val_id = cur.execute(message, (value,)).fetchone()
    val_id = list(val_id)
    return val_id


# Query della lista degli artisti
def art_list():
     conn = get_db()
     cur = conn.cursor()
     tup_lis = cur.execute("""SELECT artista FROM Artista""").fetchall()
     #trasformo la tupla ottenuta in lista.
     new_list = []
     for tup in tup_lis:
         lis=list(tup)
         new_list += lis
     return new_list

# Query della lista degli album
def alb_list():
     conn = get_db()
     cur = conn.cursor()
     tup_lis = cur.execute("""SELECT album FROM Album""").fetchall()
     new_list = []
     for tup in tup_lis:
         lis=list(tup)
         new_list += lis
     return new_list

# Query della lista dei generi
def gen_list():
     conn = get_db()
     cur = conn.cursor()
     tup_lis = cur.execute("""SELECT genere FROM Genere""").fetchall()
     new_list = []
     for tup in tup_lis:
         lis=list(tup)
         new_list += lis
     return new_list

""" Viene utilizzata nel validatore traccia_check per vedere se la traccia inserita
dall'utente è già presente in DB. Il parametro:nome serve per acquisire l'id dell'utente
attualmente connesso (idquery e userid). Poi si richiede al Db una lista delle tracce
dell'utente. Restituisce una lista delle tracce (non in forma di tupla)"""
def trac_list(nome):
     conn = get_db()
     cur = conn.cursor()
     idquery = "SELECT Utente_id FROM Dati_utente WHERE Nome=?"
     userid = id_value(idquery, nome, cur)
     tup_lis = cur.execute("SELECT canzone FROM Traccia WHERE User_id=?", userid).fetchall()
     new_list = []
     for tup in tup_lis:
         lis=list(tup)
         new_list += lis
     close_db()
     return new_list



"""********       FUNZIONI PER I VALIDATORI FORM CANZONE       *******"""

""" Se la canzone è gia presente nel DB, questa funzione la recupera con l'album e l'artista
associati ad essa per poi confrontarla nel validatore con l'album e l'artista inseriti
dall'utente. Esportata in validate.py per la funzione traccia_check che funge da
validatore per la il titolo della canzone."""
def list_song(titolo):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT Traccia.canzone, Album.album, Artista.artista FROM Traccia JOIN Album,
        Artista ON Traccia.Album_id = Album.Album_id AND Album.Artista_id = Artista.Artista_id
        WHERE canzone=?""", [titolo])
    data_song=cur.fetchall()
    new_list = []
    for tup in data_song:
        lis=list(tup)
        new_list += lis
    close_db()
    return new_list



"""********       INSERIMENTO DATI IN DB       *******
Logica inserimento Dati:
- La traccia deve essere sempre inserita nel DB. Se già presente verrà filtrata
    prima della validazione
- Artista non presente - Album non presente --> creare entrambi
- Artista non presente - ALbum presente --> creare entrambi (non è possibile
    associare l'album già presente (che è associato ad altro artista), con lartista creato)
- Artista presente - Album presente --> Se sono già associati prendere solo gli id;
    se l'album già presente è associato con altro artista, creare l'album
- Artista presente - Album non presente --> creare solo album
NOTA CHE: secondo la logica di questo programma, nel DB può esistere solo un'artista
vuoto (associato a più album); in realtà non possono esistere due nomi artisti uguali.
Invece possono esistere più album vuoti associati ognuno ad un'artista diverso."""

""" Controllo se l'artista inserito nel form dall'utente sia già presente sul DB,
inserisco l'artista nel database (se non presente) e ritorna il suo id"""
def insert_art(artista, album, cur):
    id_query = "SELECT Artista_id FROM Artista WHERE artista=?"
    if artista in art_list():
        return id_value(id_query, artista, cur)
    cur.execute("INSERT INTO Artista (artista) VALUES (?)", [artista])
    # Ricavo l'id dell'artista appena inserito (sottoforma di lista)
    values = id_value(id_query, artista, cur)
    # Aggiungo alla lista l'album
    values.append(album)
    cur.execute("INSERT INTO Album (Artista_id, album) VALUES (?,?)", values)
    return id_value(id_query, artista, cur)

""" Controllo se l'album inserito nel form dall'utente sia già presente sul DB,
richiamo la funzione insert_art per ottenere id dell'artista e inserisco l'album
con il corrispondente id dell'artista nel database (se l'album non presente).
Ritorna id dell'album."""
def insert_alb(album, artista, cur):
    # Richiamo la funzione insert_art ricavando id Artista e inserisco i valori
    # Artista_id e album in una lista
    values = insert_art(artista, album, cur)
    values.append(album)
    # Chiedo id dell'album confrontando id artista e nome album; Se id album è
    # nullo, l'album o non c'è, oppure c'è ed associato ad altro artista e
    # in entrambi i casi va creato associandolo al nuovo artista.
    cur.execute("SELECT Album_id FROM Album WHERE Artista_id=? AND album=?", values)
    albumid = cur.fetchone()
    if albumid != None:
        albumid = list(albumid)
        return albumid
    cur.execute("INSERT INTO Album (Artista_id, album) VALUES (?,?)", values)
    cur.execute("SELECT Album_id FROM Album WHERE Artista_id=? AND album=?", values)
    albumid = cur.fetchone()
    albumid = list(albumid)
    return albumid

""" Come per insert_art """
def insert_gen(genere, cur):
    id_query = "SELECT Genere_id FROM Genere WHERE genere=?"
    if genere in gen_list():
        return id_value(id_query, genere, cur)
    cur.execute("INSERT INTO Genere (genere) VALUES (?)", [genere])
    return id_value(id_query, genere, cur)

""" Inserimento della traccia nel DB con i corrispondenti id di album e genere."""
def insert_trac(artista, album, genere, traccia, filepath):
    conn = get_db()
    cur = conn.cursor()
    nome = current_user.nome
    # Richiamo l'id utente loggato da associare a tutte le tracce che inserisce nel DB
    id_query= "SELECT Utente_id FROM Dati_utente WHERE Nome=?"
    utente_id = id_value(id_query, nome, cur)
    # Creo la lista values dei valori da inserire (id album, id genere, id utente e traccia)
    values = insert_alb(album, artista, cur)
    values = values + insert_gen(genere, cur) + utente_id
    values.append(traccia)
    values.append(filepath)
    cur.execute("INSERT INTO Traccia (Album_id, Genere_id, User_id, canzone, Filepath) VALUES (?,?,?,?,?)",
        values)
    conn.commit()
    close_db(e=None)
    return

""" La funzione da esportare in views che richiama le precedenti 4 funzioni per
l'inserimento dei dati nel DB """
def main_insert(artista, album, genere, traccia, filepath):
    insert_art(artista)
    insert_trac(traccia, album, genere, artista, filepath)
    close_db(e=None)
    return



"""********       LISTA DELLE CANZONI UTENTE      *******"""

""" Lista delle canzoni dell'utente loggato. Esportata in views. Il parametro nome
serve per recuperare l'id dell'utente che, nel DB, è associato alle canzoni.
Questa lista verrà inviata al frontend."""
def lista_canzoni_utente(nome):
    conn = get_db()
    cur = conn.cursor()
    idquery = "SELECT Utente_id FROM Dati_utente WHERE Nome=?"
    userid = id_value(idquery, nome, cur)
    cur.execute("""SELECT Traccia.canzone, Album.album, Artista.artista, Genere.genere,
        Traccia.FilePath, Traccia_id FROM Traccia JOIN Album, Artista, Genere ON Traccia.Album_id =
        Album.Album_id AND Traccia.Genere_id = Genere.Genere_id
        AND Album.Artista_id = Artista.Artista_id WHERE User_id=?""", userid)
    lista_canzoni = cur.fetchall()
    close_db(e=None)
    return lista_canzoni



"""********     CANCELLA CANZONE DAL DB    *******"""

"""Cancella la canzone dal DB:
recupero del percorso (modificato) del file dal DB; modificato per permetterne
l'inserimento facilitato nel player audio. Quindi il percorso file non comincia
da SingSong, ma comincia dalla cartella static.
Poi cancello la traccia dal DB. Il parametro:nome serve ricevere l'id Utente. Le
2 istruzioni al DB (secondo SELECT e DELETE) per essere corrette devono essere legate
sia al nome della canzone che all'id utente, altrimenti si rischia di cancellare
anche canzone di altro utente
La funzione restituisce il path sottoforma di stringa. e viene esportata nelle views."""
def delete_song(song_id, nome):
    conn = get_db()
    cur = conn.cursor()
    # Prendo id utente
    idquery = "SELECT Utente_id FROM Dati_utente WHERE Nome=?"
    userid = id_value(idquery, nome, cur)
    # Trasformo id in lista e aggiungo il nome camzone
    values = list(userid)
    values.append(song_id)
    # Chiedo il percorso del file al DB
    path = cur.execute("SELECT FilePath FROM Traccia WHERE User_id=? AND Traccia_id=?",
        values).fetchone()
    cur.execute("DELETE FROM Traccia WHERE User_id=? AND Traccia_id=?",
        values)
    conn.commit()
    close_db(e=None)
    return path[0]



"""********     FUNZIONE UPDATE SONG    *******

param:title è il vecchio titolo per cercare la canzone da modificare nel DB;
param:nome è lo username per trovare la canzone in corrispondenza dello user;
param:traccia è il nuovo titolo da inserire al posto del vecchio;
param:album è il vecchio album serve per recuperare l'id dell'album e identificare
    meglio la vecchia canzone da modificare"""
def update_titolo(traccia_id, traccia):
    conn = get_db()
    cur = conn.cursor()
    # Creo una lista "values" con Traccia_id per ricercare il titolo da modificare
    values = [traccia, traccia_id]
    cur.execute("""UPDATE Traccia SET canzone = ? WHERE Traccia_id=?""", values)
    conn.commit()
    close_db(e=None)
    return

"""L'utente modifica l'album o l'artista; le logiche legate a queste modifiche rispecchiano
INSERIMENTO DATI IN DB (vedi sopra). Infatti viene usata la funzione "insert_alb", solo nel caso in cui
l'utente modifichi o album o artista.
Questi dati non vengono modificati ma creati nuovi (se non esistono).
Viene solo modificato l'id dell'album nella tabella Traccia.

param:album è l'album inserito dall'utente.
param:artista è l'artista inseerito dall'utente.
param:traccia_id è l'id della traccia che si sta modificando."""
def update_alb_id(album, artista, traccia_id):
    conn = get_db()
    cur = conn.cursor()
    values = insert_alb(album, artista, cur)
    values.append(traccia_id)
    cur.execute("""UPDATE Traccia SET Album_id = ? WHERE Traccia_id=?""", values)
    conn.commit()
    close_db(e=None)
    return

def update_gen(genere, traccia_id):
    conn = get_db()
    cur = conn.cursor()
    values = insert_gen(genere, cur)
    values.append(traccia_id)
    cur.execute("""UPDATE Traccia SET Genere_id = ? WHERE Traccia_id=?""", values)
    conn.commit()
    close_db(e=None)
    return



"""********     CANCELLO ALBUM, ARTISTA E GENERE NON UTILIZZATI    *******"""

"""Questa funzione mantiene il DB pulito eliminando album, genere e artista che non
sono collegati ad una traccia."""
def delete_not_util():
    conn = get_db()
    cur = conn.cursor()
    alb_id_list = cur.execute("SELECT Album_id FROM Traccia").fetchall()
    alb_id_list2 = cur.execute("SELECT Album_id FROM Album").fetchall()
    for id in alb_id_list2:
        if id not in alb_id_list:
            cur.execute("DELETE FROM Album WHERE Album_id=?", id)
            conn.commit()
    art_id_list = cur.execute("SELECT Artista_id FROM Album").fetchall()
    art_id_list2 = cur.execute("SELECT Artista_id FROM Artista").fetchall()
    for id in art_id_list2:
        if id not in art_id_list:
            cur.execute("DELETE FROM Artista WHERE Artista_id=?", id)
            conn.commit()
    gen_id_list = cur.execute("SELECT Genere_id FROM Traccia").fetchall()
    gen_id_list2 = cur.execute("SELECT Genere_id FROM Genere").fetchall()
    for id in gen_id_list2:
        if id not in gen_id_list:
            cur.execute("DELETE FROM Genere WHERE Genere_id=?", id)
            conn.commit()
    close_db(e=None)
    return
