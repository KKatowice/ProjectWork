from flask_sqlalchemy import SQLAlchemy
from flask import *
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DBNAME = "concessionario"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('ID')}:{os.getenv('PSW')}@"
    f"{os.getenv('H')}:{os.getenv('PRT')}/concessionario"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Motore(db.Model):
    __tablename__ = 'motori'
    id_motore = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cilindrata = db.Column(db.Numeric(10, 2))
    potenza = db.Column(db.Numeric(10, 2))
    cavalli = db.Column(db.Integer)
    carburante = db.Column(db.String(25))
    consumi = db.Column(db.Numeric(10, 2))
    emissioni = db.Column(db.Numeric(10, 2))
    serbatoio = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            'id_motore': self.id_motore,
            'cilindrata': float(self.cilindrata),
            'potenza': float(self.potenza),
            'cavalli': self.cavalli,
            'carburante': self.carburante,
            'consumi': float(self.consumi),
            'emissioni': float(self.emissioni),
            'serbatoio': float(self.serbatoio)
        }


class Marchio(db.Model):
    __tablename__ = 'marchi'
    id_marchio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45))
    foto_marchio = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_marchio': self.id_marchio,
            'nome': self.nome,
            'foto_marchio': self.foto_marchio
        }


class Auto(db.Model):
    __tablename__ = 'auto'

    id_auto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_motore = db.Column(db.Integer, db.ForeignKey('motori.id_motore'))
    id_marchio = db.Column(db.Integer, db.ForeignKey('marchi.id_marchio'))
    modello = db.Column(db.String(55))
    prezzo = db.Column(db.Numeric(10, 2))
    foto_auto = db.Column(db.String(255))
    motore = db.relationship(Motore, foreign_keys=id_motore)
    marchio = db.relationship(Marchio, foreign_keys=id_marchio)

    def to_dict(self):
        return {
            'id_auto': self.id_auto,
            'id_motore': self.id_motore,
            'id_marchio': self.id_marchio,
            'modello': self.modello,
            'prezzo': float(self.prezzo),
            'foto_auto': self.foto_auto
        }


