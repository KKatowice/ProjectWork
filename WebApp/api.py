from werkzeug.security import check_password_hash, generate_password_hash

from classAuto import *
from sys import path
import json

isFABIO = False
if not isFABIO:
    path.append(r'ProjectWork/Database')
    from ProjectWork.Database.dbUtils_aiven import *
else:
    path.append(r'Database')
    from dbUtils_aiven import *

apiBlueprint = Blueprint("apiBlueprint", __name__)

DBNAME = "concessionario"


# --auto--
@apiBlueprint.route('/api/getAuto', methods=['GET'])
def getAuto():
    page = int(request.args.get('page', default=1))
    items_per_page = 42
    offset = (page - 1) * items_per_page
    c = create_db_connection(DBNAME)


    q = f"""SELECT * FROM auto
         JOIN motori ON motori.id_motore = auto.id_motore
         JOIN marchi ON marchi.id_marchio = auto.id_marchio
         ORDER BY auto.prezzo
         LIMIT {items_per_page} OFFSET {offset};"""

    res = read_query(c, q)
    c.close()
    return res

@apiBlueprint.route('/api/getMarchio', methods=['GET'])
def getMarchio():
    page = int(request.args.get('page', default=1))
    items_per_page = 21
    offset = (page - 1) * items_per_page
    c = create_db_connection(DBNAME)

    q = f"""SELECT * FROM marchi
         ORDER BY marchi.nome
         LIMIT {items_per_page} OFFSET {offset};"""

    res = read_query(c, q)
    c.close()
    return res

@apiBlueprint.route('/api/getAutobyMarchio', methods=['GET'])
def getAutobyMarchio():
    marchio = request.args.get('marchio')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN marchi ON auto.id_marchio = marchi.id_marchio 
        JOIN motori ON auto.id_motore = motori.id_motore WHERE marchi.nome = '{marchio}'; """
    res = read_query(c, q)
    c.close()
    return res

# --tutte le auto per motore--
@apiBlueprint.route('/api/getAutobyMotori', methods=['GET'])
def getAutobyMotori():
    cilindratamax = request.args.get('cilindratamax')
    cilindratamin = request.args.get('cilindratamin')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN motori ON auto.id_motore = motori.id_motore WHERE motore.cilindrata BETWEEN '{cilindratamin}' AND '{cilindratamax}'; """
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
    q = f"""SELECT * FROM auto
        JOIN motori ON motori.id_motore = auto.motori
        JOIN marchi ON marchi.id_marchio = auto.id_marchio 
        WHERE motori.cilindrata = '{cilindrata}' AND marchi.nome = '{marca}'; """
    res = read_query(c, q)
    c.close()

    # Restituisci i risultati alla pagina web
    return render_template('risultati_ricerca.html', risultati=res)

# --PAGINA UTENTE--
@apiBlueprint.route('/api/getAutobyBudget', methods=['GET'])
def getAutobyBudget():
    num_utente = request.args.get("num_utente")
    c = create_db_connection("concessionario")
    q1 = f"""SELECT budget FROM utente WHERE id_utente = "{num_utente}"; """
    budget = read_query(c, q1)[0]['budget']
    q2 = f"""SELECT * FROM auto
         JOIN motori ON motori.id_motore = auto.id_motore
         JOIN marchi ON marchi.id_marchio = auto.id_,marchio
         WHERE auto.prezzo < {budget};"""

    res = read_query(c, q2)
    c.close()
    return res


# @apiBlueprint.route('/api/auto_filter', methods=['POST'])
def filtra_auto(data):
    from classAuto import Auto, Motore, Marchio
    print("cavalli",int(data['cavalli']))
    print("potenza",float(data['potenza']))
    print("emissioni",int(data['emissioni']))
    resultz = (Motore.query.join(Auto, Motore.id_motore == Auto.id_motore)
            .join(Marchio, Marchio.id_marchio == Auto.id_marchio)
            .filter(Marchio.nome == data['marchio'])
            .filter(Motore.carburante == data['carburante'])
            .filter(Motore.consumi <= float(data['consumi']))
            .filter(Auto.prezzo <= float(data['prezzo']))
            .filter(Motore.serbatoio >= float(data['serbatoio']))
            .filter(Motore.cilindrata >= float(data['cilindrata']))
            .filter(Motore.cavalli >= int(data['cavalli']))#tu cazzo3 mesa sempre nel value base
            .filter(Motore.potenza >= float(data['potenza']))#tu cazzo2 errore nella tranformazione a int (era float) e value base
            .filter(Motore.emissioni <= float(data['emissioni']))#tu cazzo, errore nel value base html
            ).all()
    print("dai su!!!!!!!!!!!!!\n ", resultz)
    result = []
    for x in resultz:
        print(x.to_dict())
        result.append(x.to_dict())
    
    """ print("in filtra",data)
    q = (Auto.query.join(Motore, Motore.id_motore == Auto.id_motore)
            .join(Marchio, Marchio.id_marchio == Auto.id_marchio)
            .filter(Marchio.nome == data['marchio'])
            .filter(Motore.carburante == data['carburante'])
            .filter(Motore.consumi < float(data['consumi']))
            .filter(Motore.emissioni < float(data['emissioni']))
            .filter(Auto.prezzo < float(data['prezzo']))
            .filter(Motore.serbatoio > float(data['serbatoio']))
            .filter(Motore.potenza > int(data['potenza']))
            .filter(Motore.cilindrata > int(data['cilindrata']))
            .filter(Motore.cavalli > int(data['cavalli'])))
    
    result = q.all() """
    if result:
        r = {'data':result, 'success': True}
    else:
        r = {'data': [], 'success': False}
    return json.dumps(r)
#funziona per i test#http://127.0.0.1:5000/auto?filtro=filtrate&marchio=alfa-romeo&carburante=Diesel%20&consumi=6&emissioni=150&prezzo=99000&serbatoio=58&potenza=100.3&cilindrata=2&cavalli=100


@apiBlueprint.route('/api/login', methods=['POST'])
def login():
    print("gagag")
    connessione = create_db_connection(DBNAME)
    try:
        data = request.get_json()
        print("data dentro python login",data)
        email = data['email']
        password = data['password']
        q = f"""SELECT password FROM utenti WHERE email = '{email}';"""
        data1 = read_query(connessione, q)[0]
        #print(data1, password)
        if len(data1) > 0:
            #print(check_password_hash(str(data1['password']), password))
            pswcheck = check_password_hash(str(data1['password']), password)
            if pswcheck:
                session['utente'] = data['email']
                return {'success':True}
            else:
                return {'success':False}
        else:
            return {'success':False}
    except Exception as e:
        print(e)
        return {'success':False}
    finally:
        connessione.close()

@apiBlueprint.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    connessione = create_db_connection(DBNAME)
    nome = data['nome']
    cognome = data['cognome']
    eta = data['eta']
    sesso = data['sesso']
    email = data['email']
    password = generate_password_hash(data['password'])
    cap = data['cap']
    q = f"""INSERT INTO utenti(nome, cognome, eta, sesso, email, password, cap)
                         VALUES('{nome}','{cognome}','{eta}','{sesso}','{email}','{password}','{cap}')"""
    try:
        execute_query(connessione, q)
        return {'success':True}

    except Exception as e:
        print(e)
        return {'success':False}


@apiBlueprint.route('/api/aggiungiPreferiti', methods=['PUT'])
def aggiungiPreferiti():
    data = request.get_json()
    c = create_db_connection(DBNAME)
    id_auto = read_query(c, f"SELECT id_auto FROM auto WHERE modello = '{data['auto']}';")[0]['id_auto']
    id_utente = read_query(c, f"SELECT id_utente FROM utenti WHERE email = '{data['utente']}';")[0]['id_utente']
    verifica = read_query(c,f"SELECT * FROM preferenze WHERE id_auto = {id_auto} AND id_utente = {id_utente};")
    if len(verifica) == 0:
        q = f"""INSERT INTO preferenze(id_auto, id_utente) VALUES({id_auto}, {id_utente})"""
        execute_query(c,q)
        return {'success': True}
    else:
        return {'success': False}



def getPreferenze(utente):
    c = create_db_connection(DBNAME)
    q = f"SELECT id_auto FROM preferenze join utenti on preferenze.id_utente = utenti.id_utente where utenti.email = '{utente}';"
    lista_id_auto = read_query(c, q)
    lista_finale = []
    for x in lista_id_auto:
        q1 = f"""SELECT * FROM auto JOIN motori JOIN marchi
                ON auto.id_motore=motori.id_motore AND auto.id_marchio=marchi.id_marchio
                WHERE id_auto = {x['id_auto']};"""
        info_auto = read_query(c, q1)[0]
        lista_finale.append(info_auto)
    c.close()
    return lista_finale

@apiBlueprint.route('/api/deletePreferito', methods=['DELETE'])
def deletePreferito():
    c = create_db_connection(DBNAME)
    user = session.get('utente')
    auto = request.get_json()
    id_utente = read_query(c, f"SELECT id_utente FROM utenti WHERE email = '{user}';")[0]['id_utente']
    q = f"DELETE FROM preferenze WHERE id_auto = {auto['id_auto']} AND id_utente = {id_utente};"
    r = execute_query(c,q)
    c.close()
    if r:
        return {"success":True}
    else:
        return {"success":False}
