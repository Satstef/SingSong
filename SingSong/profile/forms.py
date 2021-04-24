from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import DataRequired, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Optional
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from .validate import traccia_check, traccia_check_alb, filename_match
from SingSong.auth.validate import strip_filter


# Non è possibile usare la classe BaseForm con il filtro perchè sembra entrare
# in conflitto ocn il FileField, ma non capisco il perchè.
class CanzoneForm(FlaskForm):
    file = FileField('Select a mp3 file', validators=
        [FileRequired(message='Upload a mp3 file'),
        FileAllowed(['mp3'], 'Invalid file. Only mp3 file'), filename_match])
    titolo = StringField('Song title', filters=[strip_filter], validators=
        [InputRequired(message='Required field'), DataRequired(message=
        'Invalid input')])
    album = StringField('Album', filters=[strip_filter], validators=
        [Optional(strip_whitespace=True), traccia_check_alb])
    artista = StringField('Artist', filters=[strip_filter], validators=
        [Optional(strip_whitespace=True), traccia_check])
    genere = StringField('Genere', filters=[strip_filter],
        validators=[Optional(strip_whitespace=True)])
    submit = SubmitField('Done')

# I validatori di questo form sono in Javascript: file profile.js nella cartella
# static. La funzione è validateForm()
class AggiornaCanzone(FlaskForm):
    tit_id = StringField()
    alb_hide = StringField()
    art_hide = StringField()
    gen_hide = StringField()
    titolo = StringField('Song title', filters=[strip_filter], validators=
        [DataRequired(message='Invalid input')])
    album = StringField('Album', filters=[strip_filter], validators=
        [Optional(strip_whitespace=True)])
    artista = StringField('Artist', filters=[strip_filter], validators=
        [Optional(strip_whitespace=True)])
    genere = StringField('Genere', filters=[strip_filter],
        validators=[Optional(strip_whitespace=True)])
    submit = SubmitField('Update')
