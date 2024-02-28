import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import r2_score

from ProjectWork.Database.dbUtils_aiven import *

c = create_db_connection(DBNAME)
q = """SELECT auto.modello, auto.prezzo, marchi.nome, motori.carburante, motori.cavalli, motori.cilindrata,
    motori.consumi, motori.emissioni, motori.potenza, motori.serbatoio
    FROM auto JOIN marchi JOIN motori
    ON auto.id_marchio = marchi.id_marchio AND auto.id_motore = motori.id_motore;"""
ldd = read_query(c, q)

df = pd.DataFrame(ldd)

# print(df.head())
print(df.info()) #TODO quasi tutti object, da cambiare(prezzo,cilindrata,consumi,emissioni,potenza,serbatoio), ma ora ho sonno vediamo domani
# print(df.isnull().sum()) niente valori null

