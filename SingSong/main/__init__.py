from flask import Blueprint
main = Blueprint('main', 'SingSong')
from .views import home
