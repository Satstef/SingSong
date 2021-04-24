from flask import Blueprint
prof = Blueprint('profile', 'SingSong')
from . import views
