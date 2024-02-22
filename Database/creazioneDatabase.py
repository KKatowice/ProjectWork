from dbUtils_aiven import *

connection = create_server_connection()
create_database(connection, "CREATE DATABASE concessionario")
c = create_db_connection()

marchi = """CREATE TABLE marchi(
            id_marchio int PRIMARY KEY AUTO_INCREMENT,
            nome varchar(45) UNIQUE NOT NULL,
            foto_marchio varchar(255))"""

motore = """CREATE TABLE motori(
            id_motore int PRIMARY KEY AUTO_INCREMENT,
            cilindrata decimal(10,1),
            potenza decimal(10,1),
            cavalli int,
            carburante varchar(255),
            consumi decimal(10,2),
            emissioni decimal(10,2),
            serbatoio decimal(10,1)
            )"""

auto = """CREATE TABLE auto(
            id_auto int PRIMARY KEY AUTO_INCREMENT,
            id_motore int,
            id_marchio int,
            modello varchar(100),
            prezzo decimal(12,2), 
            foto_auto varchar(255),
            FOREIGN KEY (id_motore) REFERENCES motori(id_motore) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (id_marchio) REFERENCES marchi(id_marchio) ON DELETE CASCADE ON UPDATE CASCADE)"""

utenti = """CREATE TABLE utenti(
            id_utente int PRIMARY KEY AUTO_INCREMENT,
            nome varchar(55) NOT NULL,
            cognome varchar(55) NOT NULL,
            eta int(11) NOT NULL CHECK(eta>0 AND eta<120),
            sesso varchar(55) NOT NULL CHECK(sesso = 'maschio' or sesso ='femmina' or sesso = 'altro'),
            email varchar(55) UNIQUE NOT NULL,
            password varchar(55) UNIQUE NOT NULL,
            cap varchar(6),
            budget int)"""

preferenze = """CREATE TABLE preferenze(
                id_preferenze int PRIMARY KEY AUTO_INCREMENT,
                id_auto int,
                id_utente int,
                FOREIGN KEY (id_auto) REFERENCES auto(id_auto) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (id_utente) REFERENCES utenti(id_utente) ON DELETE CASCADE ON UPDATE CASCADE)"""

utenti_bloccati = """CREATE TABLE utenti_bloccati(
                id_utente_bloccato int PRIMARY KEY AUTOINCREMENT,
                id_utente int,
                email varchar(55) UNIQUE NOT NULL,
                password varchar(55) UNIQUE NOT NULL,
                FOREIGN KEY (id_utente) REFERENCES utente('id_utente') ON DELETE CASCADE ON UPDATE CASCADE)"""


execute_query(c, marchi)
execute_query(c, motore)
execute_query(c, auto)
execute_query(c, utenti)
execute_query(c, preferenze)
execute_query(c, utenti_bloccati)
