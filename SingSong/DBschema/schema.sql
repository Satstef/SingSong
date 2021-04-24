---------------- TABELLA DATI UTENTI ---------------------

CREATE TABLE IF NOT EXISTS Dati_utente (
  Utente_id INTEGER PRIMARY KEY NOT NULL,
  Nome TEXT UNIQUE NOT NULL,
  Email TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  Conferma INTEGER DEFAULT 0,
  Confermato_il	TEXT
);


---------------- TABELLE DATI CANZONE ---------------------

CREATE TABLE IF NOT EXISTS Artista (
  Artista_id INTEGER PRIMARY KEY  NOT NULL,
  artista TEXT
);

CREATE TABLE IF NOT EXISTS Album (
  Album_id INTEGER PRIMARY KEY NOT NULL,
  Artista_id INTEGER,
  album TEXT,
  FOREIGN KEY (Artista_id)
  REFERENCES Artista (Artista_id)
      ON UPDATE CASCADE
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Genere (
  Genere_id INTEGER PRIMARY KEY  NOT NULL,
  genere TEXT
);

CREATE TABLE IF NOT EXISTS Traccia (
  Traccia_id INTEGER PRIMARY KEY  NOT NULL,
  Album_id INTEGER,
  Genere_id INTEGER,
  canzone TEXT NOT NULL,
  User_id INTEGER,
  FilePath TEXT NOT NULL,
  FOREIGN KEY (Album_id)
  REFERENCES Album (Album_id)
      ON UPDATE CASCADE
      ON DELETE CASCADE
  FOREIGN KEY (Genere_id)
  REFERENCES Genere (Genere_id)
      ON UPDATE CASCADE
      ON DELETE CASCADE
  FOREIGN KEY (User_id)
  REFERENCES Dati_utente (Utente_id)
);
