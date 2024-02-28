from sys import path

from flask import Blueprint

from appADMIN import *

# Aggiungi le import necessarie per le funzioni del database
path.append(r'ProjectWork/Database')

adminBlueprint = Blueprint("adminBlueprint", __name__)

# Includi le API della tua web app qui
from ProjectWork.WebApp.api import *  # Aggiorna con i nomi corretti delle funzioni API


# @adminBlueprint.route('/admin/getAuto', methods=['GET'])
# def admin_getAuto():
#     result = getAuto()  # Chiama la funzione API getAuto della tua web app
#     return jsonify(result)  # Restituisci i risultati in formato JSON
#
#
# @adminBlueprint.route('/admin/getMarchio', methods=['GET'])
# def admin_getMarchio():
#     result = getMarchio()  # Chiama la funzione API getMarchio della tua web app
#     return jsonify(result)  # Restituisci i risultati in formato JSON
#
#
# @adminBlueprint.route('/admin/getAutobyMarchio', methods=['GET'])
# def admin_getAutobyMarchio():
#     result = getAutobyMarchio()  # Chiama la funzione API getAutobyMarchio della tua web app
#     return jsonify(result)  # Restituisci i risultati in formato JSON
#
#
# @adminBlueprint.route('/admin/getAutobyMotori', methods=['GET'])
# def admin_getAutobyMotori():
#     result = getAutobyMotori()  # Chiama la funzione API getAutobyMotori della tua web app
#     return render_template()  # Restituisci i risultati in formato JSON

#AUTO
@apiBlueprint.route('/api/aggiungi/auto', methods=['POST'])
def aggiungi_auto():
    if session.get("utente") == "admin":
        c = create_db_connection(DBNAME)
        get_json = request.get_json()
        modello = get_json['modello']
        marchio = get_json['marchio']
        prezzo = get_json['prezzo']
        foto_auto = get_json['foto_auto']
        cilindrata = get_json['cilindrata']
        potenza = get_json['potenza']
        cavalli = get_json['cavalli']
        carburante = get_json['carburante']
        consumi = get_json['consumi']
        emissioni = get_json['emissioni']
        serbatoio = get_json['serbatoio']
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
            id = read_query(c,id_query)
            id2_query = f"""SELECT id_marchio FROM marchi WHERE nome = '{marchio}'"""
            id2= read_query(c,id2_query)
            q1 = f"""INSERT INTO auto Values('{id}','{id2}','{modello}','{prezzo}','{foto_auto}');"""
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
    id = f"""SELECT id_motore FROM auto WHERE modello = '{modello}' """
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
               SET marchio = '{marchio}', prezzo = '{prezzo}', foto_auto = '{foto_auto}'
               WHERE modello = '{modello}'
               ;
               """
    q2 = f"""
               UPDATE motori
               SET cilindrata = '{cilindrata}', potenza = '{potenza}',
                cavalli = '{cavalli}', carburante = '{carburante}',
                carburante = '{carburante}', consumi = '{consumi}',
                emissioni = '{emissioni}', serbatoio = '{serbatoio}'
                WHERE id_motore = '{id}'
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
        nome = data["nome"]
        cognome = data["cognome"]
        email = data["email"]
        q = f"""SELECT FROM utenti
                                WHERE nome = '{nome}',cognome = '{cognome}',email = '{email}';"""

        q2 = f"""DELETE FROM utenti
                        WHERE nome = '{nome}',cognome = '{cognome}',email = '{email}';"""
        verifica = read_query(c, q)
        r = execute_query(c, q2)

        if len(verifica) > 0:
            if r:
                return {'success': True}
            else:
                return {'success': False}
        else:
            return {'success': False}




@apiBlueprint.route('/api/aggiungi/utente', methods=['POST'])
def aggiungi_utenti():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        nome = nome = data["nome"]
        cognome =  data["cognome"]
        eta = data["eta"]
        email = nome = data["email"]
        password = nome = data["password"]
        sesso = data["sesso"]
        provincia = data["provincia"]
        budget = data["budget"]
        admin = 0
        registrazione = 0
        q_verifica = f"""SELECT FROM utenti WHERE nome ={nome} AND cognome = {cognome} AND  eta = {eta} AND email = {email} AND password = {password} AND sesso = {sesso} AND provincia = {provincia} AND budget = {budget}"""
        q = f"""INSERT INTO utenti Values('{nome}','{cognome}','{eta}','{email}','{password}','{sesso}','{provincia}','{budget}','{admin}','{registrazione}')"""
        verifica = read_query(c, q_verifica)
        r = execute_query(c, q)
        if len(verifica) == 0:
            if r:
                return {'success': True}
            else:
                return {'success': False}

        else:
            return {'Error': True}



#MARCHIO

@apiBlueprint.route('/api/aggiugi/marchio', methods=['POST'])
def aggiugi_marchio():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        nome = data["nome"]
        foto_marchio = data["foto_marchio"]
        q_verifica = f"""SELECT FROM marchi WHERE nome = {nome} AND foto_marchio = {foto_marchio} ;"""
        q = f"""INSERT INTO utenti Values('{nome}','{foto_marchio}')"""
        verifica = read_query(c, q_verifica)
        r = execute_query(c, q)
        if len(verifica) == 0:
            if r:
                return {'success': True}
            else:
                return {'success': False}

        else:
            return {'Error': True}



@adminBlueprint.route('/api/rimuovi/marchio', methods=['POST'])
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