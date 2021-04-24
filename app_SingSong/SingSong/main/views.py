import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, flash, redirect, url_for
from . import main

@main.route('/')
def home():
    return render_template('index.html')
