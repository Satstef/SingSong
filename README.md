# SingSong app

![alt text](https://github.com/Satstef/SingSong/blob/14678c487eea336f52df05662b487f0dd0ddddd3/app_SingSong/SingSong/static/Home.png?raw=true)

![alt text](https://github.com/Satstef/SingSong/blob/16cd10808399f55a33f8d40e79788c8b96e0b9f0/app_SingSong/SingSong/static/user-profile.png?raw=true)

## 1. General description
This is a **web running** application used to store your favourites songs and listen to them.  
Some Backend programming work(Python):
- register an account and login safely;
- sending email with confirmation token;
- store datas in sqlite3 Database;
- creating users personal folder to store uploaded files;

Some Frontend programming work: 
- creating forms; 
- creating user profile pages;
- Making user interact with the app (insert song information, update them, listen to music);
If you may find this code helpful for your works, I will be glad to give more information about.


## 2. How the app works on internet
App works in a very basic way. The user has to register an account by giving his/her name, email and choosing
one password. An email with a link will be send to him/her. After confirmating the
account by clicking on the link, the user can login in his/her profile.
User can upload mp3 files (only mp3 files are allowed) and enter song informations (title, album, artist and genre).
He/She is now ready to listen the song uploaded.


## 3. Download and configuration

### 3.1 virtualenv and App name
To set configuration of the application on your machine is not complicated at all. It just requires
a little bit of your patience and time.
The application has been programmed with Python version 3.8 and flask framework.
The Database used is sqlite3; this library is already included in Python. If you want a Database GUI you need to download it here https://sqlitebrowser.org/dl/

After download you need a virtual enviroment where to install dependencies:
- From shell go in **app_SingSong** directory and create your own virtual enviroment.
- Activate the virtualenv. I Will use **venv** name as example for the virtualenv.
- Install all required packages (see requirements file) using pip (or pip3).

`(venv) $ pip3 install -r requirements.txt`

- From shell, staying in **app_SingSong** directory, launch command:

`(venv) $ export FLASK_APP=SingSong`

`(venv) $ export FLASK_ENV=development`

This last one runs the application on local server in development enviroment.
This enviroment is useful if you want to modify the app code. In fact the debug system
becomes active and tells you where exactly is the code error (in case is there some).


### 3.2 Secret key, Database and Email
Please follow these instruction in the order they are.

- Set the **SECRET_KEY** variable. If you are in development enviroment, you may utilize the given SECRET_KEY to test the application. In Production you need to change the key and give another one. From shell:
`(venv) $ export SECRET_KEY=b'secretkey'`

- Initialize Database **sqlite3** from shell.
Database file (Database.db) and his schema (schema.sql), by default are in same
directory called **DBschema**. You can find it under **app_SingSong/SingSong** directory.
In DBschema you won't find the database file yet, only schema.sql is there. To initialize
the DB file:
  1. move the **DBschema** directory anywhere on your System.
  2. tell the application where is the folder to create the DB file.
  From shell set the DATABASE enviroment variable with the abspath to **DBschema** directory:

  `(venv) $ export DATABASE_URL=abspath to the folder/DBschema`

  3. tell the application where is the schema.sql file. We suppose is in the same folder.
  of DB file:

  `(venv) $ export DB_SCHEMA_URL=abspath to the folder/DBschema`

  4. create DB file:

  `(venv) $ flask init-db`

  If everything was ok, on your terminal should appear **Database creato con successo** and Database.db file in **DBschema** directory

- Email settings.
  When the user register his/her account an email with a confirmation link will be send.
  You need to setup the email sender configuration (see config.py file).
  How to do that is very simple.

  In **Development** configuration (just follow this configuration and leave the **Production** one; to better understand how to change cnfiguration go to 3.4 paragraph) the mail server is set by default on googlemail.
  All you need is gmail account. After that, you need to tell the application
  your googlemail account:

  `(venv) $ export MAIL_USERNAME=your googlemail`

  `(venv) $ export MAIL_PASSWORD=your password`

  In **Production** configuration (don't do this now; this is only when you deploy the app) you can set the email server, the port and TLS.

  `$ export MAIL_SERVER=your mail server`

  `$ export MAIL_PORT=your port number`

  `$ export MAIL_USE_TLS=True or False`
  
  **IMPORTANT NOTE:** on some Shell if you input your email password ending with some
  symbol (for example double Exclamation point), the command shell will mess up.
  But don't worry, you'll notice it, and change password.

### 3.3 Launch your localhost server and run the app
Now you can start local server:

`(venv) $ flask run`

Will run your local server on port 5000.
To see the application running open any browser and type

`localhost:5000` or `127.0.0.1:5000`

This is the home page of the application.


### 3.4 Development and Production configuration
The application has 2 configuration types (see **config.py** file):
- **Development** if you are running the application on your localhost server in development enviroment, means you are bringing changes to the code and testing it. In this case the Development configuration is adviced.
- **Production** configuration is the one, if you want to deploy the app on server with a domain name.

According to what you want to do (improve and test or deploy the application), you
need to set the proper configuration. By default the application is set on **Development** configuration.
If you need to change, do it in this way:
  1. Open in your IDE the file: `app_SingSong/SingSong/__init__.py` (the factory function).
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


## 4. Something more to know
- The Database has relational structure among all tables (One to many relations).
- When a user register and click on confirmation link in his/her email, a personal
folder (named with user name) will be created in the application in the path:
SingSong/static/upload_song. Here all his/her mp3 files will be stored. The path
to the folder is stored in Database.db file under **Dati_utente** table.

