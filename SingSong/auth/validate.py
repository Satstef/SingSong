import sqlite3
from .db_conn import nome_list, email_list, password_call
from werkzeug.security import check_password_hash
from wtforms.validators import ValidationError, StopValidation



"""********         FILTRI        ********"""

"""Filtro customizzato (che viene aggiunto alla classe Meta (guarda in basso)
per eliminare gli spazi vuoti all'inizio e alla fine. Inoltre controlla che non siano
inseriti solo spazi vuoti nel campo. Inserito nella classe Meta (vedi in basso)"""
def strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        if value.strip() == "":
            raise ValidationError('Required field')
        else:
            return value.strip()



"""********        VALIDATORI FORM REGISTRA       *******"""

""" Le due funzioni successive controllano che il Nome  e la mail inseriti in fase di
registrazione non siano già presenti nel DB. Sono validatori customizzati.
Dalla riga 'tup_lis = cur.fetchall()', i dati ricevuti dal DB (che sono tuple) vengono
trasformati in liste e quindi possono essere manipolati. """
def nome_check(form, field):
    tup_lis = nome_list()
    new_list = []
    for tup in tup_lis:
        lis=list(tup)
        new_list += lis
    if field.data in new_list:
        raise ValidationError("Name already in use, choose another one")


def email_check(form, field):
    tup_lis = email_list()
    new_list = []
    for tup in tup_lis:
        lis=list(tup)
        new_list += lis
    if field.data in new_list:
        raise ValidationError("Email already in use")


"""********        VALIDATORI FORM LOGIN       *******"""

"""Controllo che la mail inserita in fase di login sia presente nel database.
La funzione email_list richiama le mail dal DB e la tupla ottenuta viene
trasformata in lista per essere confrontata con la mail inserita."""
def email_check_login(form, field):
    tup_lis = email_list()
    new_list = []
    for tup in tup_lis:
        lis=list(tup)
        new_list += lis
    if field.data not in new_list:
        raise ValidationError("Invalid Email")

"""Con password_call viene richiamata la password (hash) nel DB in corrispondenza
della riga della mail inserita. check_password_hash permette di confrontare l'hash
password del DB con la password inserita dall'utente. Se corrispondono ritorna True
e la validazione è confermata."""
def password_check_login(form,field):
    email = form.email.data
    hash_pass = password_call(email)
    if check_password_hash(hash_pass, form.password.data) == False:
        raise ValidationError("Invalid password")
