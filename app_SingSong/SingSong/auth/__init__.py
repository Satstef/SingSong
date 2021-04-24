from flask import Blueprint
auth = Blueprint('auth', 'SingSong')
from .views import registra, login
from .forms import BaseForm
