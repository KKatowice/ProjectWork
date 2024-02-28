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


if __name__ == '__main__':
    app.run(debug=True)
