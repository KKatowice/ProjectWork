from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://avnadmin:AVNS_R6OpJnjvrGcYTzCaBPv@team2-proj-project-work.a.aivencloud.com/concessionario'  # Modifica l'URI del tuo database
app.config['SECRET_KEY'] = 'a'  # Modifica con una chiave segreta sicura
db = SQLAlchemy(app)

# Definisci il tuo modello SQLAlchemy


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://avnadmin:AVNS_R6OpJnjvrGcYTzCaBPv@team2-proj-project-work.a.aivencloud.com/concessionario'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


#Definizione dei modelli delle tabelle

class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca_id = db.Column(db.Integer, db.ForeignKey('marchi.id'), nullable=False)
    modello = db.Column(db.String(100), nullable=False)


class Marchi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


class Motori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


class Utenti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)

class UtenteBloccato(db.Model):
    __tablename__ = 'utenti_bloccati'

    id_utente_bloccato = Column(Integer, primary_key=True, autoincrement=True)
    id_utente = Column(Integer, ForeignKey('utenti.id_utente'))
    email = Column(String(55), unique=True, nullable=False)
    password = Column(String(55), nullable=False)
    utente = relationship("Utente", backref="utenti_bloccati")
# Visualizzazione dei dati
@app.route('/')
def admin():

    return render_template('admin.html' )
@app.route('/auto')
def show_auto():
    auto = Auto.query.all()
    return render_template('auto.html', auto=auto)


@app.route('/marchi')
def show_marchi():
    marchi = Marchi.query.all()
    return render_template('marchi.html', marchi=marchi)


@app.route('/motori')
def show_motori():
    motori = Motori.query.all()
    return render_template('marchi.html', marchi=motori)


@app.route('/utenti')
def show_utenti():
    utenti = Utenti.query.all()
    return render_template('marchi.html', marchi=utenti)


# Ripeti lo stesso per le altre tabelle

# Modifica dei dati

@app.route('/auto/<int:id>/aggiungi', methods=['GET', 'POST'])
def aggiungi_auto(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_auto'))
    return render_template('aggiungi_auto.html', auto=auto)


@app.route('/marchi/<int:id>/aggiungi', methods=['GET', 'POST'])
def aggiungi_marchi(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_marchi'))
    return render_template('aggiungi_marchi.html', auto=auto)


@app.route('/motori/<int:id>/aggiungi', methods=['GET', 'POST'])
def aggiungi_motori(id):
    motore = Motori.query.get(id)
    if request.method == 'POST':
        motore.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('show_motori'))
    return render_template('aggiungi_motori.html', motore=motore)


@app.route('/utenti/<int:id>/aggiungi', methods=['GET', 'POST'])
def aggiungi_utenti(id):
    utente = Utenti.query.get(id)
    if request.method == 'POST':
        utente.username = request.form['username']
        db.session.commit()
        return redirect(url_for('show_utenti'))
    return render_template('aggiungi_utenti.html', utente=utente)


# Cancellazione dei dati

@app.route('/auto/<int:id>/cancella', methods=['POST'])
def cancella_auto(id):
    auto = Auto.query.get(id)
    db.session.delete(auto)
    db.session.commit()
    return redirect(url_for('show_auto'))


@app.route('/marchi/<int:id>/cancella', methods=['POST'])
def cancella_marchi(id):
    marchio = Marchi.query.get(id)
    db.session.delete(marchio)
    db.session.commit()
    return redirect(url_for('show_marchi'))


@app.route('/motori/<int:id>/cancella', methods=['POST'])
def cancella_motori(id):
    motore = Motori.query.get(id)
    db.session.delete(motore)
    db.session.commit()
    return redirect(url_for('show_motori'))


@app.route('/utenti/<int:id>/cancella', methods=['POST'])
def cancella_utenti(id):
    utente = Utenti.query.get(id)
    db.session.delete(utente)
    db.session.commit()
    return redirect(url_for('show_utenti'))


@app.route('/auto/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_auto(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_auto'))
    return render_template('modifica_auto.html', auto=auto)


@app.route('/marchi/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_marchi(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_marchi'))
    return render_template('modifica_marchi.html', auto=auto)


@app.route('/motori/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_motori(id):
    motore = Motori.query.get(id)
    if request.method == 'POST':
        motore.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('show_motori'))
    return render_template('modifica_motori.html', motore=motore)


@app.route('/utenti/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_utenti(id):
    utente = Utenti.query.get(id)
    if request.method == 'POST':
        utente.username = request.form['username']
        db.session.commit()
        return redirect(url_for('show_utenti'))
    return render_template('modifica_utenti.html', utente=utente)




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

            return {"cancellato": True}
        else:
            return {"cancellato": False}

    except Exception as e:
        # In caso di errore, restituisci una risposta JSON con indicazione dell'errore
        return {"success": False, "error": str(e)}


if __name__ == '__main__':
    app.run(debug=True)