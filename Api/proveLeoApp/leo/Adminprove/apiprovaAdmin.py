@app.route('api/auto/<int:id>/aggiorna', methods=['GET', 'POST'])
def aggiorna_auto(id_auto, id_motore):
    c = create_db_connection(DBNAME)
    try:
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
                   WHERE id_auto = '{id_auto}';
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

        if len(r) > 0 and len(r2) > 0:
            session['admin'] = True
            return {"success": True}
        else:
            return {"success": False}

    except Exception as e:
        # In caso di errore, restituisci una risposta JSON con indicazione dell'errore
        return {"success": False, "error": str(e)}


@app.route('api/aggiungi_auto', methods=['GET', 'POST'])
def aggiungi_auto():
    c = create_db_connection(DBNAME)
    try:
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
        if len(r1) > 0 and len(r2) > 0:
            session['admin'] = True
            return {"success": True}
        else:
            return {"success": False}
    except Exception as e:
        # In caso di errore, restituisci una risposta JSON con indicazione dell'errore
        return {"success": False, "error": str(e)}


@app.route('api/elimina_auto', methods=['GET', 'POST'])
def elimina_auto():
    c = create_db_connection(DBNAME)
    try:
        data = request.get_json()
        modello = data["modello"]
        q = f"""DELETE FROM auto
            WHERE modello = '{modello}';"""
        r = execute_query(c, q)

        if len(r) == None:
            session['admin'] = True
            return {"cancellato": True}
        else:
            return {"cancellato": False}

    except Exception as e:
        # In caso di errore, restituisci una risposta JSON con indicazione dell'errore
        return {"success": False, "error": str(e)}