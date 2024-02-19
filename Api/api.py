from flask import Blueprint, request, render_template
from sys import path
path.append('create db')
from Database.dbUtils import *




DBNAME = "concessionario"

apiBlueprint = Blueprint("apiBlueprint", __name__)

# --auto--
@apiBlueprint.route('/api/getAuto', methods=['GET'])
def getAuto():
    page = int(request.args.get('page', default=1))
    items_per_page = 20
    offset = (page - 1) * items_per_page
    c = create_db_connection(DBNAME)
    print(c)

    q = f"""SELECT * FROM auto "
         JOIN motori ON motori.id_motore = auto.id_motore "
         JOIN marchi ON marchi.id_marchio = auto.id_,marchio"
         ORDER BY auto.prezzo"
         LIMIT {items_per_page} OFFSET {offset};"""

    res = read_query(c, q)
    c.close()
    return res

# --tutte le auto per motore--
@apiBlueprint.route('/api/getAutobyMotori', methods=['GET'])
def getAutobyMotori():
    cilindratamax = request.args.get('cilindratamax')
    cilindratamin = request.args.get('cilindratamin')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN motori ON auto.id_motore = motori.id_motore WHERE motore.cilindrata BETWEEN "{cilindratamin}" AND "{cilindratamax}"; """
    res = read_query(c, q)
    c.close()
    return res

# @apiBlueprint.route('/api/get', methods=['GET'])
# def Top10Film():
#     c = create_db_connection(DBNAME)
#     q = "SELECT * FROM film ORDER BY Average_rating DESC LIMIT 10"
#     res = read_query(c, q)
#     c.close()
#     return res

@apiBlueprint.route('/api/getAutobyMarchio', methods=['GET'])
def getAutobyMarchio():
    marchio = request.args.get('marchio')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN marchio ON auto.id_marchio = marchio.id_marchio WHERE marchio.nome = "{marchio}"; """
    res = read_query(c, q)
    c.close()
    return res


# --CRUD--
# datetime formato pe date: 'YYYY-MM-DD HH:MM:SS'

@apiBlueprint.route('/api/getRicerca', methods=['GET'])
def getRicerca():
    form_data = request.form
    # Estrai i dati dal form
    cilindrata = form_data.get('cilindrata')
    marca = form_data.get('marchio')
    capacità_serbatoio = form_data("capacità_serbatoio")

    # Esegui la ricerca nel database basata sui dati del form
    c = create_db_connection(DBNAME)
    q = f"""SELECT * FROM auto WHERE nome = "{nome}" AND marca = "{marca}"; """
    res = read_query(c, q)
    c.close()

    # Restituisci i risultati alla pagina web
    return render_template('risultati_ricerca.html', risultati=res)


@apiBlueprint.route('/api/getAutobyBudget', methods=['GET'])
def getAutobyBudget():
    form_data = request.form
    num_utente = form_data("num_utente")
    c = create_db_connection(DBNAME)
    q1 = f"""SELECT  budget FROM utente WHERE id_utente = "{num_utente}"; """
    q2 = f"""SELECT * FROM auto "
         JOIN motori ON motori.id_motore = auto.id_motore "
         JOIN marchi ON marchi.id_marchio = auto.id_,marchio"
         WHERE auto.prezzo < utente.budget;"""
    res = read_query(c, q1)
    res = read_query(c, q2)
    c.close()
    return render_template('risultati_ricerca.html', risultati=res)




