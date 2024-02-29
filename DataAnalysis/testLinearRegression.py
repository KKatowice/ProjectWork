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
from sklearn.metrics import confusion_matrix

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

df = df.loc[~((df['potenza'] > 50) & (df['potenza'] < 500))]
df = df.loc[~((df['cavalli'] > 50) & (df['cavalli'] < 500))]


cat=["nome", "carburante"]
for x in cat:
    encoder = LabelEncoder()
    df[x]= encoder.fit_transform(df[x])
scalare = MinMaxScaler()
lol = df.values.tolist()
lista_scalata = scalare.fit_transform(lol)
df_scalato = pd.DataFrame(lista_scalata, columns=['prezzo', 'nome', 'carburante', 'cavalli', 'cilindrata', 'consumi', 'emissioni', 'potenza', 'serbatoio'])



fig, axes = plt.subplots(3,3 , figsize=(24,18))
fig.tight_layout(pad=5.0)
axes = axes.flatten()
features = df.columns[1:]
for i in range(len(features)):
    sns.scatterplot(data=df, x=features[i], y="prezzo", ax=axes[i])
    plt.xlabel(str(features[i]))
    plt.ylabel('Prezzo')
    print(features[i])

plt.show()

target = df_scalato['prezzo']
training = df_scalato.drop(['prezzo', 'nome', 'cilindrata', 'carburante', 'consumi', 'serbatoio', 'emissioni'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(training, target, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train,y_train)
cose = pd.DataFrame([{'cavalli': 0.134, 'potenza': 0.134}])

preds=model.predict(X_test)
print(preds)
print(r2_score(preds,y_test))




model = RandomForestRegressor()
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(preds,y_test))

model = KNeighborsRegressor(n_neighbors=2)
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(preds,y_test))
