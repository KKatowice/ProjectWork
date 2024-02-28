from werkzeug.security import check_password_hash, generate_password_hash

from classAuto import *
from sys import path
import json
# isFABIO = True
isFABIO = True
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


from decimal import Decimal
from classAuto import Auto, Motore, Marchio
def fixaRess(diz):
    diz = diz.copy()
    max_values_query = db.session.query(
        db.func.max(Motore.cilindrata).label('cilindrata'),
        db.func.max(Motore.potenza).label('potenza'),
        db.func.max(Motore.cavalli).label('cavalli'),
        db.func.max(Motore.consumi).label('consumi'),
        db.func.max(Motore.emissioni).label('emissioni'),
        db.func.max(Motore.serbatoio).label('serbatoio')
        ).first()
    min_values_query = db.session.query(
        db.func.min(Motore.cilindrata).label('cilindrata'),
        db.func.min(Motore.potenza).label('potenza'),
        db.func.min(Motore.cavalli).label('cavalli'),
        db.func.min(Motore.consumi).label('consumi'),
        db.func.min(Motore.emissioni).label('emissioni'),
        db.func.min(Motore.serbatoio).label('serbatoio')
        ).first()
    max_values = max_values_query._asdict()
    min_values = min_values_query._asdict()
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",max_values, min_values)
    for k,v in diz.items():
        if v == "0" or v == "0.0" or v == 0:
        #data['consumi'] - data['prezzo'] - data['emissioni'] - tutto il resto check >=
            if k == 'consumi' or k == 'emissioni':
                diz[k] = max_values[k]
            elif k == 'serbatoio' or k == 'cilindrata' or k == 'cavalli' or k == 'potenza':
                #print(max_values[k], type(max_values[k]))
                diz[k] = min_values[k]
            elif k == 'prezzo':
                diz[k] = 100000000
        print(v)
        if isinstance(diz[k],Decimal):
            diz[k] = float(diz[k])

        
    return diz



@apiBlueprint.route('/api/auto_filter', methods=['POST'])
def filtra_auto(data=None):
    if data == None:
        data = request.get_json()
    print("\n-------prima->->-->---",data)
    data = fixaRess(data)
    print(data,"\n-<-<-,--dopo--------\n")
    resultz = (Motore.query.join(Auto, Motore.id_motore == Auto.id_motore)
            .join(Marchio, Marchio.id_marchio == Auto.id_marchio)
            .filter(Motore.consumi <= float(data['consumi']))
            .filter(Auto.prezzo <= float(data['prezzo']))
            .filter(Motore.emissioni <= float(data['emissioni']))
            .filter(Motore.serbatoio >= float(data['serbatoio']))
            .filter(Motore.cilindrata >= float(data['cilindrata']))
            .filter(Motore.cavalli >= int(data['cavalli']))
            .filter(Motore.potenza >= float(data['potenza']))
            )
    if data['marchio'] != 'tutti':
        resultz = resultz.filter(Marchio.nome == data['marchio'])
    if data['carburante'] != 'tutti ':
        resultz = resultz.filter(Motore.carburante == data['carburante'])
    resultz = resultz.add_columns(Auto).all()
    print("dai su!!!!!!!!!!!!!\n ", resultz)
    result = []
    for x in resultz:
        d1 = x[0].to_dict()
        d2 = x[1].to_dict()
        d3 = {**d1, **d2}
        splt = d3['modello'].split(" ")
        d3['nome'] = splt[0]
        result.append(d3)

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
        q1 = f"""SELECT password FROM utenti WHERE email = '{email}';"""
        q2 = f"""SELECT password FROM utenti_bloccati WHERE email = '{email}';"""
        q_admin = f"""SELECT admin FROM utenti WHERE email = '{email}';"""
        data1 = read_query(connessione, q1)[0]
        data2 = read_query(connessione, q2)
        data_admin = read_query(connessione, q_admin )
        print(data1, password, data2)

        if len(data1) > 0 and (data2 == None or len(data2) == 0) :
            print('entrato')
            #print(check_password_hash(str(data1['password']), password))
            pswcheck = check_password_hash(str(data1['password']), password)
            if pswcheck:
                if data_admin[0]['admin'] == 1:
                    print('check superato per admin')
                    session["utente"] = "admin"
                else:

                    print('check superato per utente')
                    session['utente'] = data['email']
                return {'success':True}

            else:
                print('sorry')
                return {'success': False, 'bloccato': False}
        else:
            if len(data2) > 0:
                return {'success':False, 'bloccato': True}
            else:

                return {'success': False, 'bloccato': False}
    except Exception as e:
        print(e)
        return {'success':False}
    finally:
        connessione.close()

# @apiBlueprint.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     connessione = create_db_connection(DBNAME)
#     nome = data['nome']
#     cognome = data['cognome']
#     eta = data['eta']
#     sesso = data['sesso']
#     email = data['email']
#     password = generate_password_hash(data['password'])
#     cap = data['cap']
#     q = f"""INSERT INTO utenti(nome, cognome, eta, sesso, email, password, cap)
#                          VALUES('{nome}','{cognome}','{eta}','{sesso}','{email}','{password}','{cap}')"""
#     try:
#         execute_query(connessione, q)
#         return {'success':True}
#
#     except Exception as e:
#         print(e)
#         return {'success':False}


@apiBlueprint.route('/api/utentebloccato', methods=['POST'])
def utentebloccato():
    connessione = create_db_connection(DBNAME)
    data = request.get_json()
    email = data['email']
    q = f"""INSERT INTO utente_bloccato(email) VALUES('{email}')"""
    execute_query(connessione,q)


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
    print(lista_finale)
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


@apiBlueprint.route('/api/deleteAccount', methods=['DELETE'])
def deleteAccount():
    c = create_db_connection(DBNAME)
    email = session.get('utente')
    q = f"DELETE FROM utenti WHERE email = '{email}';"
    r = execute_query(c, q)
    c.close()
    if r:
        session['utente'] = None
        return {"success": True}
    else:
        return {"success": False}

# CRUD ADMIN

@apiBlueprint.route('/api/aggiungi_auto', methods=['POST'])
def aggiungi_auto():
    if session.get("utente") == "admin":
        c = create_db_connection(DBNAME)
        data = request.get_json()
        modello = data['modello']
        marchio = data['marchio']
        prezzo = data['prezzo']
        foto_auto = data['foto_auto']
        cilindrata = data['cilindrata']
        potenza = data['potenza']
        cavalli = data['cavalli']
        carburante = data['carburante']
        consumi = data['consumi']
        emissioni = data['emissioni']
        serbatoio = data['serbatoio']
        q_ver = f"""SELECT * FROM motori WHERE cilindrata = '{cilindrata}' AND potenza = '{potenza}' AND cavalli = '{cavalli}'
         AND carburante = '{carburante}' AND consumi = '{consumi}' AND emissioni = '{emissioni}' 
         AND serbatoio = '{serbatoio}';"""
        if len(q_ver)==0:
            q2 = f"""INSERT INTO motori(cilindrata, potenza, cavalli, carburante, consumi, emissioni, serbatoio) 
            Values('{cilindrata}','{potenza}','{cavalli}','{carburante}','{consumi}','{emissioni}','{serbatoio}');"""
            r2 = execute_query(c, q2)
            id_query = f"""SELECT id_motore FROM motori WHERE cilindrata = '{cilindrata}' AND potenza = '{potenza}' AND cavalli = '{cavalli}'
                    AND carburante = '{carburante}' AND consumi = '{consumi}' AND emissioni = '{emissioni}' 
                    AND serbatoio = '{serbatoio}';"""
            id = read_query(c,id_query)[0]['id_motore']
            id2_query = f"""SELECT id_marchio FROM marchi WHERE nome = '{marchio}'"""
            id2= read_query(c,id2_query)[0]['id_marchio']
            q1 = f"""INSERT INTO auto(id_motore, id_marchio, modello, prezzo, foto_auto) 
                VALUES('{id}','{id2}','{modello}','{prezzo}','{foto_auto}');"""
            r1 = execute_query(c, q1)
            if r1 and r2:
                return {"success": True}
            else:
                return {"success": False}

@apiBlueprint.route('/api/modifica/auto', methods=['GET', 'POST'])
def modifica_auto():
    c = create_db_connection(DBNAME)
    data = request.get_json()
    modello = data["modello"]
    new_modello = data['new_modello']
    id_motore = read_query(c, f"""SELECT id_motore FROM auto WHERE modello = '{modello}' """)[0]['id_motore']
    marchio = data["marchio"]
    prezzo = data["prezzo"]
    foto_auto = data["foto_auto"]
    cilindrata = data["cilindrata"]
    potenza = data["potenza"]
    cavalli = data["cavalli"]
    carburante = data["carburante"]
    consumi = data["consumi"]
    emissioni = data["emissioni"]
    serbatoio = data["serbatoio"]
    q = f"""
               UPDATE auto
               SET id_marchio = '{marchio}', modello = '{new_modello}',
               prezzo = '{prezzo}', foto_auto = '{foto_auto}'
               WHERE modello = '{modello}'
               ;
               """
    q2 = f"""
               UPDATE motori
               SET cilindrata = '{cilindrata}', potenza = '{potenza}',
                cavalli = '{cavalli}', carburante = '{carburante}',
                carburante = '{carburante}', consumi = '{consumi}',
                emissioni = '{emissioni}', serbatoio = '{serbatoio}'
                WHERE id_motore = '{id_motore}'
               ;
               """
    r = execute_query(c, q)
    r2 = execute_query(c, q2)
    c.close()
    if r and r2:
        return {"success": True}
    else:
        return {"success": True}



@apiBlueprint.route('/api/rimuovi/auto', methods=['POST'])
def cancella_auto():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        modello = data["modello"]
        q = f"""DELETE FROM auto
                    WHERE modello = '{modello}';"""
        r = execute_query(c, q)
        if r:
            return {'success':True}
        else:
            return {'success':False}



#UTENTI
@apiBlueprint.route('/api/rimuovi/utente', methods=['POST'])
def cancella_utenti():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        email = data["email"]
        q = f"""SELECT * FROM utenti
                                WHERE email = '{email}';"""

        q2 = f"""DELETE FROM utenti
                        WHERE email = '{email}';"""
        verifica = read_query(c, q)


        if len(verifica) > 0:
            r = execute_query(c, q2)
            if r:
                return {'success': True}
            else:
                return {'success': False}
        else:
            return {'success': False}

#MARCHIO

@apiBlueprint.route('/api/aggiugi/marchio', methods=['POST'])
def aggiugi_marchio():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        nome = data["nome"]
        foto_marchio = data["foto_marchio"]
        q_verifica = f"""SELECT FROM marchi WHERE nome = '{nome}';"""
        q = f"""INSERT INTO marchi(nome, foto_marchio) VALUES('{nome}','{foto_marchio}')"""
        verifica = read_query(c, q_verifica)
        if len(verifica) == 0:
            r = execute_query(c, q)
            if r:
                return {'success': True}
            else:
                return {'success': False}

        else:
            return {'Error': True}



@apiBlueprint.route('/api/rimuovi/marchio', methods=['POST'])
def rimuovi_marchio():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        nome = data["nome"]
        q = f"""DELETE FROM marchi
                        WHERE nome = '{nome}';"""
        r = execute_query(c, q)
        if r:
            return {'success': True}
        else:
            return {'success': False}