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
q = """SELECT auto.prezzo, marchi.nome, motori.carburante, motori.cavalli, motori.cilindrata,
    motori.consumi, motori.emissioni, motori.potenza, motori.serbatoio
    FROM auto JOIN marchi JOIN motori
    ON auto.id_marchio = marchi.id_marchio AND auto.id_motore = motori.id_motore;"""
ldd = read_query(c, q)

df = pd.DataFrame(ldd)

# print(df.head())
 #TODO quasi tutti object, da cambiare(prezzo,cilindrata,consumi,emissioni,potenza,serbatoio), ma ora ho sonno vediamo domani
# print(df.isnull().sum()) niente valori null

df['prezzo'] = pd.to_numeric(df['prezzo'])
df['cavalli'] = pd.to_numeric(df['cavalli'])
df['cilindrata'] = pd.to_numeric(df['cilindrata'])
df['consumi'] = pd.to_numeric(df['consumi'])
df['emissioni'] = pd.to_numeric(df['emissioni'])
df['potenza'] = pd.to_numeric(df['potenza'])
df['serbatoio'] = pd.to_numeric(df['serbatoio'])


cat=["nome", "carburante"]
for x in cat:
    encoder = LabelEncoder()
    df[x]= encoder.fit_transform(df[x])
scalare = MinMaxScaler()
lol = df.values.tolist()
lista_scalata = scalare.fit_transform(lol)
print(lista_scalata[:1])
df_scalato = pd.DataFrame(lista_scalata, columns=['prezzo', 'nome', 'carburante', 'cavalli', 'cilindrata', 'consumi', 'emissioni', 'potenza', 'serbatoio'])



fig, axes = plt.subplots(3,3 , figsize=(24,18))
fig.tight_layout(pad=5.0)
axes = axes.flatten()
features = df_scalato.columns[1:]
for i in range(len(features)):
    sns.scatterplot(data=df_scalato, x=features[i], y="prezzo", ax=axes[i])
    plt.xlabel(str(features[i]))
    plt.ylabel('Prezzo')
    print(features[i])

plt.show()
