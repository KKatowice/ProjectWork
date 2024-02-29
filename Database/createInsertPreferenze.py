from dbUtils_aiven import *
from random import choice

c = create_db_connection('concessionario')

user = read_query(c, "SELECT id_utente, budget from utenti;")
auto = read_query(c, "SELECT id_auto, prezzo FROM auto;")

for utente in user:
    if utente['budget'] == None:
        utente['budget'] = 0

lista_utente_auto = []

for i in range(len(user)):
    lista_utente_auto.append({'id_utente': user[i]['id_utente'], 'auto': []})
    for y in auto:
        if y['prezzo'] <= user[i]['budget']:
            lista_utente_auto[i]['auto'].append(y['id_auto'])

lista_upload = []

for e in lista_utente_auto:
    u = e['id_utente']
    a = choice(e['auto'])
    aa = choice(e['auto'])
    aaa = choice(e['auto'])
    lista_upload.append((u, a,))
    if aa != a:
        lista_upload.append((u, aa,))
    if aaa != aa and aaa != a:
        lista_upload.append((u, aaa,))

q = "INSERT INTO preferenze(id_utente, id_auto) VALUES(%s, %s);"
execute_many_query(c,q, lista_upload)
