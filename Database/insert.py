from dbUtils import *
import json

#Apro i due file json
c = create_db_connection("concessionario")
data = json.load(open("../Datasets_Scraping/completo.json"))
users = json.load(open("../Datasets_Scraping/utenti.json"))

#Inserimento dei marchi
def insert_marchi():
    for elem in data.keys():
        query = f"""INSERT INTO marchi(nome, foto_marchio) VALUES('{elem}', "{data[elem]['imglink']}")"""
        execute_query(c,query)


#Inserimento degli utenti
def insert_users():
    lista = []
    for elem in users.keys():
        t = (users[elem]['nome'],users[elem]['cognome'],users[elem]['eta'],users[elem]['sesso'], users[elem]['email'],users[elem]['cap'],users[elem]['budget'])
        lista.append(t)
    query = f"""INSERT INTO utenti(nome, cognome, eta, sesso, email, cap, budget) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    execute_many_query(c,query,lista)

def insert_motori():
    l = []
    for motore in data.keys():
        t = (data[motore]['Pdisplacement:'], data[motore][''],data[motore]['HP:'],
             data[motore]['Fuel:'], data[motore]['Combined:'],data[motore]['CO2 Emissions (Combined):'], data[motore]['Fuel capacity:'])
        l.append(t)
    query = f"""INSERT INTO motori(cilindrata, potenza, cavalli, carburante,
            consumi, emissioni, serbatoio) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    execute_many_query(c,query,l)

def insert_auto():
    l = []
    i = 1
    for auto in data.keys():
        t = (data[auto])
        for x in data[auto].items():
            t.add(x['']) #PREZZO
            t.add(x['']) #FOTO
        numero = read_query(c,query=f"""SELECT id_marchio FROM marchi WHERE nome = {auto}""")[0]['id_marchio']
        t.add(numero)
        t.add(i)
        i += 1
        l.append(t)
    query = f"""INSERT INTO auto(modello, prezzo, foto_auto, id_marchio, id_motore) VALUES(%s,%s,%s,%s,%s)"""
    execute_many_query(c, query, l)



insert_marchi()
# insert_users()
# insert_motori()
insert_auto()

