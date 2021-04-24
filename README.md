# SingSong app

## General description
This is a **web running** application used to store your favourites songs and listen to them.  
The programming part is about:
- registering an account and login safely;
- sending email with confirmation token;
- creating user profile page, upload files and create interactions between user and
the machine (user can insert data, update them, listen to music);
- creating users personal folder to store uploaded files
If you may find this code helpful for your works, I will be glad to give more information about.


## How the app works on internet
The user has to register an account by giving his/her name, email and choosing
one password. An email with a link will be send to him/her. After confirmating the
account by clicking on the link, the user can login in his/her profile.
User can upload mp3 files (only mp3 files are allowed) and describe the song with
title, album, artist and genre.
He/She is now ready to listen the song uploaded.


## After downloading the application
To set the application on your machine is not complicated at all. It just requires
a little bit of your patience and time.
The application has been programmed with Python version 3.8 and flask framework.

After download you need a virtual enviroment where install dependencies:
- From shell go in **app_SingSong** directory and create your own virtual enviroment.
- Activate the virtualenv. I Will use **venv** name as example for the virtualenv.
- Install all required packages (see requirements file) using pip (or pip3).
`(venv) $ pip3 install -r requirements.txt`
- From shell, staying in **app_SingSong** directory, launch command:
`(venv) $ export FLASK_APP=SingSong`
`(venv) $ export FLASK_ENV=development`
This last one runs the application on local server in Development mode.
This mode is useful if you want to modify the app code. In fact the debug system
becomes active and tells you where exactly is the code error (in case is there some).
`(venv) $ flask run`
Will run your local server on port 5000.
To see the application running open any browser and type
`localhost:5000` or `127.0.0.1:5000`
This is the home page of the application.


## Development and Production
The application has 2 configuration types (see **config.py** file):
- **Development** if you want to bring changes to the code and test it on your
localhost server;
- **Production** if you want to deploy it.
These 2 modes have different configuration settings, so please read carefully the
following **Setup the application** part.


## Setup the application
Please follow these instruction in the order they are.
- Set the **Development** or **Production** configuration.
According to what you want to do (improve and test or deploy the application), you
need to set the proper configuration. By default it is on **Development** mode.
If you need to change, do it in this way:
  1. Open in your IDE the file: SingSong/__init__.py (the factory function).
  2. Change the **config_class**
  ```python
  def create_app(config_class=Development):
      app = Flask('SingSong')
  ```

  with this
  ```python
  def create_app(config_class=Production):
      app = Flask('SingSong')
  ```
- Set the **SECRET_KEY** variable. If in Development configuration, you may utilize the given SECRET_KEY to test the application. In Production you need to change the key and give another one. From shell:
`(venv) $ export SECRET_KEY=b'secretkey'`

- Initialize Database **sqlite3** from shell.
Database file (Database.db) and his schema (schema.sql), by default are in same
directory called **DBschema**. You can find it under **SingSong** directory.
In DBschema you won't find the database file yet, only schema is there. To initialize
the DB file:
  1. move the **DBschema** directory anywhere on your System.
  2. tell the application where is the folder to create the DB file.
  From shell just insert the abspath without the **DBschema** directory part:
  
  `(venv) $ export DATABASE_URL=abspath to the folder`
  
  3. tell the application where is the schema.sql file. We suppose is in the same folder
  of DB file:
  
  `(venv) $ export DB_SCHEMA_URL=abspath to the folder`
  
  4. create DB file:

  `(venv) $ flask init-db`

- Email settings.
When the user register his/her account an email with a confirmation link will be send.
You need to setup the email sender configuration (see config.py file).
How to do that is very simple.
In **Development** mode the mail server is configurated by default on googlemail.
First you need an account on gmail. After that, you need to tell the application
your googlemail account:
`(venv) $ export MAIL_USERNAME=your googlemail`
`(venv) $ export MAIL_PASSWORD=your password`
**IMPORTANT NOTE:** on some Shell if you input your email password ending with some
symbol (for example double Exclamation point), the command shell will mess up.
But don't worry, you'll notice it, and change password.


In **Production** mode you can set the email server, the port and TLS.
`$ export MAIL_SERVER=mail server`
`$ export MAIL_PORT=port number`
`$ export MAIL_USE_TLS=True or False`

#### Something more to know
- The Database has relational structure among all tables (One to many relations).
- When a user register and click on confirmation link in his/her email, a personal
folder (named with user name) will be created in the application in the path:
SingSong/static/upload_song. Here all his/her mp3 files will be stored. The path
to the folder is stored in DB **Dati_utente** table.

