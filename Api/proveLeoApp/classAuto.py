from flask_sqlalchemy import SQLAlchemy
from provaApp import app
db = SQLAlchemy(app)

class Auto(db.Model):
    __tablename__ = 'auto'

    id_auto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_motore = db.Column(db.Integer)
    id_marchio = db.Column(db.Integer)
    modello = db.Column(db.String(55))
    anno = db.Column(db.Integer)
    carburante = db.Column(db.String(25))
    consumi = db.Column(db.Numeric(10, 2))
    emissioni = db.Column(db.Numeric(10, 2))
    serbatoio = db.Column(db.Numeric(10, 2))
    prezzo = db.Column(db.Numeric(10, 2))


    motori = db.relationship('motori', backref='auto', foreign_keys=[id_motore])
    marchi = db.relationship('marchi', backref='auto', foreign_keys=[id_marchio])

class Motore(db.Model):
    __tablename__ = 'motori'
    id_motore = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cilindrata = db.Column(db.Integer)
    potenza = db.Column(db.Integer)
    cavalli = db.Column(db.Integer)

