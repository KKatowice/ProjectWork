from sys import path

from flask import Blueprint

from appADMIN import *

# Aggiungi le import necessarie per le funzioni del database
path.append(r'ProjectWork/Database')

adminBlueprint = Blueprint("adminBlueprint", __name__)

# Includi le API della tua web app qui
from ProjectWork.WebApp.api import *  # Aggiorna con i nomi corretti delle funzioni API


@adminBlueprint.route('/admin/getAuto', methods=['GET'])
def admin_getAuto():
    result = getAuto()  # Chiama la funzione API getAuto della tua web app
    return jsonify(result)  # Restituisci i risultati in formato JSON


@adminBlueprint.route('/admin/getMarchio', methods=['GET'])
def admin_getMarchio():
    result = getMarchio()  # Chiama la funzione API getMarchio della tua web app
    return jsonify(result)  # Restituisci i risultati in formato JSON


@adminBlueprint.route('/admin/getAutobyMarchio', methods=['GET'])
def admin_getAutobyMarchio():
    result = getAutobyMarchio()  # Chiama la funzione API getAutobyMarchio della tua web app
    return jsonify(result)  # Restituisci i risultati in formato JSON


@adminBlueprint.route('/admin/getAutobyMotori', methods=['GET'])
def admin_getAutobyMotori():
    result = getAutobyMotori()  # Chiama la funzione API getAutobyMotori della tua web app
    return render_template()  # Restituisci i risultati in formato JSON






@apiBlueprint.route('/marchi/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_marchi(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_marchi'))
    return render_template('modifica_marchi.html', auto=auto)


@apiBlueprint.route('/motori/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_motori(id):
    motore = Motori.query.get(id)
    if request.method == 'POST':
        motore.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('show_motori'))
    return render_template('modifica_motori.html', motore=motore)






@apiBlueprint.route('/api/aggiungi_auto', methods=['GET', 'POST'])
def aggiungi_auto():
    c = create_db_connection(DBNAME)
    data = request.get_json()
    modello = data["modello"]
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
    q1 = f"""INSERT INTO auto Values('{modello}','{marchio}','{cilindrata}','{prezzo}','{foto_auto}');"""
    q2 = f"""INSERT INTO motori Values('{potenza}','{cavalli}','{carburante}','{consumi}','{emissioni}','{serbatoio}');"""
    r1 = execute_query(c, q1)
    r2 = execute_query(c, q2)
    if r1 and r2:
        return {"success": True}
    else:
        return {"success": False}

@apiBlueprint.route('/api/modifica_auto', methods=['GET', 'POST'])
def modifica_auto():
    c = create_db_connection(DBNAME)
    if session.get("utente") == "admin":
        data = request.get_json()
        modello = data["modello"]
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
                   SET modello = '{modello}', marchio = '{marchio}', prezzo = '{prezzo}', foto_auto = '{foto_auto}'
                   ;
                   """
        q2 = f"""
                   UPDATE motori
                   SET cilindrata = '{cilindrata}', potenza = '{potenza}',
                    cavalli = '{cavalli}', carburante = '{carburante}',
                    carburante = '{carburante}', consumi = '{consumi}',
                    emissioni = '{emissioni}', serbatoio = '{serbatoio}'
                   ;
                   """
        r = execute_query(c, q)
        r2 = execute_query(c, q2)
        c.close()
        if r and r2:
            return {"success": True}
        else:
            return {"success": True}


# Cancellazione dei dati

@apiBlueprint.route('/api/cancella_auto', methods=['POST'])
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




@adminBlueprint.route('/marchi/<int:id>/cancella', methods=['POST'])
def cancella_marchi(id):
    marchio = Marchi.query.get(id)
    db.session.delete(marchio)
    db.session.commit()
    return redirect(url_for('show_marchi'))


@adminBlueprint.route('/motori/<int:id>/cancella', methods=['POST'])
def cancella_motori(id):
    motore = Motori.query.get(id)
    db.session.delete(motore)
    db.session.commit()
    return redirect(url_for('show_motori'))


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

