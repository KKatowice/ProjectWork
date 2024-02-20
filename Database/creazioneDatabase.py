from dbUtils import *

connection = create_server_connection()
create_database(connection, "CREATE DATABASE concessionario")
c = create_db_connection("concessionario")

marchi = """CREATE TABLE marchi(
            id_marchio int PRIMARY KEY AUTO_INCREMENT,
            nome varchar(45) UNIQUE NOT NULL,
            foto_marchio varchar(255))"""

motore = """CREATE TABLE motori(
            id_motore int PRIMARY KEY AUTO_INCREMENT,
            cilindrata int,
            potenza int,
            cavalli int)"""

auto = """CREATE TABLE auto(
            id_auto int PRIMARY KEY AUTO_INCREMENT,
            id_motore int,
            id_marchio int,
            modello varchar(55),
            anno int,
            carburante varchar(25),
            consumi decimal(10,2),
            emissioni decimal(10,2),
            serbatoio decimal(10,2),
            prezzo decimal(10,2), 
            foto_auto varchar(255),
            FOREIGN KEY (id_motore) REFERENCES motori(id_motore) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (id_marchio) REFERENCES marchi(id_marchio) ON DELETE CASCADE ON UPDATE CASCADE)"""

utenti = """CREATE TABLE utenti(
            id_utente int PRIMARY KEY AUTO_INCREMENT,
            nome varchar(55) NOT NULL,
            cognome varchar(55) NOT NULL,
            email varchar(55) UNIQUE NOT NULL,
            cap varchar(6),
            budget int)"""

preferenze = """CREATE TABLE preferenze(
                id_preferenze int PRIMARY KEY AUTO_INCREMENT,
                id_auto int,
                id_utente int,
                FOREIGN KEY (id_auto) REFERENCES auto(id_auto) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (id_utente) REFERENCES utenti(id_utente) ON DELETE CASCADE ON UPDATE CASCADE)"""

execute_query(c, marchi)
execute_query(c, motore)
execute_query(c, auto)
execute_query(c, utenti)
execute_query(c, preferenze)
