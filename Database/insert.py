from dbUtils_aiven import *
import json
import re

#Apro i due file json
c = create_db_connection()
data = json.load(open("../Datasets_Scraping/completo_wPrices_cleaner.json"))
users = json.load(open("../Datasets_Scraping/utenti.json"))

#Inserimento dei marchi
def insert_marchi():
    for elem in data.keys():
        query = f"""INSERT INTO marchi(nome, foto_marchio) VALUES('{elem}', '{data[elem]["imglink"]}');"""
        execute_query(c,query)


#Inserimento degli utenti
def insert_users():
    lista = []
    for elem in users.keys():
        t = (users[elem]['nome'],users[elem]['cognome'],users[elem]['eta'],users[elem]['sesso'], users[elem]['email'],users[elem]['password'],users[elem]['cap'],users[elem]['budget'])
        lista.append(t)
    query = f"""INSERT INTO utenti(nome, cognome, eta, sesso, email,password, cap, budget) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
    execute_many_query(c,query,lista)

def insert_motori():
    l = []
    for marchio in data.keys():
        for elem in data[marchio].keys():
            if elem != "imglink":
                for motore in data[marchio][elem].keys():
                    if motore == "engines":
                        for auto in data[marchio][elem][motore].keys():
                            x = data[marchio][elem][motore][auto]
                            if x.get('Pdisplacement'):
                                try:
                                    cil = re.findall(r'\d+\.\d+', x['Pdisplacement'])[0]
                                except:
                                    cil = "2.0"
                            else:
                                cil = "2.0"
                            if x.get('HP'):
                                cav = x['HP']
                            else:
                                cav = "150"
                            if x.get('Power:'):
                                pot = x['Power:'].split(" ")[0]
                            else:
                                pot = str(int(cav)/1.36)
                            if x.get('Combined:'):
                                cons = x['Combined:'].split("(")[1].split(" ")[0]
                            else:
                                cons = "6"
                            if x.get('CO2 Emissions (Combined):'):
                                emiss = x['CO2 Emissions (Combined):'].split(" ")[0]
                            else:
                                emiss = "130"
                            if x.get('Fuel capacity:'):
                                serb = x['Fuel capacity:'].split("(")[1].split(" ")[0]
                            else:
                                serb = "50"
                            if x.get('Fuel:'):
                                carb = x['Fuel:']
                            else:
                                carb = "/"
                            t = (cil, pot, cav, carb, cons, emiss, serb)
                            l.append(t)
    query = f"""INSERT INTO motori(cilindrata, potenza, cavalli, carburante,
            consumi, emissioni, serbatoio) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    execute_many_query(c,query,l)


def insert_auto():
    i = 1
    l = []
    lista = []
    for marchio in data.keys():
        numero = read_query(c, query=f"""SELECT id_marchio FROM marchi WHERE nome = '{marchio}';""")[0]['id_marchio']
        for elem in data[marchio].keys():
            if elem != "imglink":
                im = data[marchio][elem]["car_imglink"]
                pr = str(data[marchio][elem]["price"])
                if pr == 'None' or pr == None:
                    pr = "0.00"
                """ if len(pr) >= 10:
                    print("wtf", pr, elem) """
                for motore in data[marchio][elem]["engines"]:
                    nome = data[marchio][elem]["engines"].keys()
                    for e in nome:
                        if e not in lista:
                            
                            lista.append(e)
                            t = (numero, im, pr, e, i)
                            i += 1
                            l.append(t)
    #l1 = l[:(len(l)//2)]
    #l2 = l[(len(l)//2):]
    query = f"""INSERT INTO auto(id_marchio, foto_auto, prezzo, modello, id_motore) VALUES(%s,%s,%s,%s,%s)"""
    execute_many_query(c, query, l)
    #execute_many_query(c, query, l2)

q1 = """SET FOREIGN_KEY_CHECKS = 0;"""
q2= """ SET FOREIGN_KEY_CHECKS = 1"""
# execute_query(c,q1)
# insert_marchi()
insert_users()
# insert_motori()
# insert_auto()
# execute_query(c,q2)








