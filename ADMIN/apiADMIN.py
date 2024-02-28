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


@adminBlueprint.route('/auto/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_auto(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_auto'))
    return render_template('modifica_auto.html', auto=auto)


@adminBlueprint.route('/marchi/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_marchi(id):
    auto = Auto.query.get(id)
    if request.method == 'POST':
        auto.marca_id = request.form['marca_id']
        auto.modello = request.form['modello']
        db.session.commit()
        return redirect(url_for('show_marchi'))
    return render_template('modifica_marchi.html', auto=auto)


@adminBlueprint.route('/motori/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_motori(id):
    motore = Motori.query.get(id)
    if request.method == 'POST':
        motore.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('show_motori'))
    return render_template('modifica_motori.html', motore=motore)


@adminBlueprint.route('/utenti/<int:id>/modifica', methods=['GET', 'POST'])
def modifica_utenti(id):
    utente = Utenti.query.get(id)
    if request.method == 'POST':
        utente.username = request.form['username']
        db.session.commit()
        return redirect(url_for('show_utenti'))
    return render_template('modifica_utenti.html', utente=utente)


# Cancellazione dei dati

@adminBlueprint.route('/auto/<int:id>/cancella', methods=['POST'])
def cancella_auto(id):
    auto = Auto.query.get(id)
    db.session.delete(auto)
    db.session.commit()
    return redirect(url_for('show_auto'))


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


@adminBlueprint.route('/utenti/<int:id>/cancella', methods=['POST'])
def cancella_utenti(id):
    utente = Utenti.query.get(id)
    db.session.delete(utente)
    db.session.commit()
    return redirect(url_for('show_utenti'))
