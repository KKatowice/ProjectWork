from ProjectWork.Database.dbUtils_aiven import *
import pandas as pd

c = create_db_connection(DBNAME)
q = """SELECT auto.prezzo, marchi.nome, motori.carburante, motori.cavalli, motori.cilindrata,
    motori.consumi, motori.emissioni, motori.potenza, motori.serbatoio
    FROM auto JOIN marchi JOIN motori
    ON auto.id_marchio = marchi.id_marchio AND auto.id_motore = motori.id_motore;"""
ldd = read_query(c, q)

df = pd.DataFrame(ldd)

df.to_csv('Dati_auto.csv', index=False)
