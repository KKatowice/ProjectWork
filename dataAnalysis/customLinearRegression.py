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
from statistics import mean
from math import sqrt, pow
def predittore(x_train, y_train, x_test): # Accetta solo liste di numeri
    if not isinstance(x_train, list):
        raise TypeError("Accetta solo una lista per x_train")
    if not isinstance(y_train, list):
        raise TypeError("Accetta solo una lista per y_train")
    if not isinstance(x_test, list):
        raise TypeError("Accetta solo una lista per x_test")
    for x in x_train:
        if not isinstance(x, (int, float)):
            raise TypeError("Ogni elemento di x_train deve essere un numero")
    for y in y_train:
        if not isinstance(y, (int, float)):
            raise TypeError("Ogni elemento deve di y_train essere un numero")
    for x in x_test:
        if not isinstance(x, (int, float)):
            raise TypeError("Ogni elemento deve di x_test essere un numero")
    x_medio = mean(x_train)
    y_medio = mean(y_train)
    lista_scarti_x = []
    lista_scarti_y = []
    for x in x_train:
        scarto = x - x_medio
        lista_scarti_x.append(scarto)
    for y in y_train:
        scarto = y - y_medio
        lista_scarti_y.append(scarto)
    prodotto_scarti = []
    for i in range(len(lista_scarti_x)):
        prodotto = lista_scarti_x[i] * lista_scarti_y[i]
        prodotto_scarti.append(prodotto)
    b = sum(prodotto_scarti)/pow(sum(lista_scarti_x), 2)
    a = y_medio - (b*x_medio)
    lista_predizioni = []
    for x in x_test:
        y = a + (b * x)
        lista_predizioni.append(y)
    quadrato_scarti_x = []
    quadrato_scarti_y = []
    for x in lista_scarti_x:
        quadrato = pow(x, 2)
        quadrato_scarti_x.append(quadrato)
    for y in lista_scarti_y:
        quadrato = pow(y, 2)
        quadrato_scarti_y.append(quadrato)
    s_x = sqrt((sum(quadrato_scarti_x)/(len(quadrato_scarti_x)-1)))
    s_y = sqrt((sum(quadrato_scarti_y)/(len(quadrato_scarti_y)-1)))
    r = (s_x / s_y) * b
    r = round(r)
    r_quadro = pow(r, 2)
    # Fare il check per r_quadro, eventualmente
    return [lista_predizioni, r, r_quadro]

def check_predizioni(y_test):
    pass


c = create_db_connection(DBNAME)
q = """SELECT auto.prezzo, marchi.nome, motori.carburante, motori.cavalli, motori.cilindrata,
    motori.consumi, motori.emissioni, motori.potenza, motori.serbatoio
    FROM auto JOIN marchi JOIN motori
    ON auto.id_marchio = marchi.id_marchio AND auto.id_motore = motori.id_motore;"""
ldd = read_query(c, q)

df = pd.DataFrame(ldd)
df['prezzo'] = pd.to_numeric(df['prezzo'])
df['cavalli'] = pd.to_numeric(df['cavalli'])
df['cilindrata'] = pd.to_numeric(df['cilindrata'])
df['consumi'] = pd.to_numeric(df['consumi'])
df['emissioni'] = pd.to_numeric(df['emissioni'])
df['potenza'] = pd.to_numeric(df['potenza'])
df['serbatoio'] = pd.to_numeric(df['serbatoio'])
df = df.loc[~((df['potenza'] > 50) & (df['potenza'] < 500))]
df = df.loc[~((df['cavalli'] > 50) & (df['cavalli'] < 500))]

scalare = MinMaxScaler()
df = df.drop(['nome', 'carburante'], axis=1)
colonne = df.columns
df_scalato = scalare.fit_transform(df.values.tolist())
df_scalato = pd.DataFrame(df_scalato, columns=colonne)


prezzo_y = df_scalato['prezzo'].tolist()
cavalli_x = df_scalato['cavalli'].tolist()
potenza_x = df_scalato['potenza'].tolist()
consumi_x = df_scalato['consumi'].tolist()
emissioni_x = df_scalato['emissioni'].tolist()
serbatoio_x = df_scalato['serbatoio'].tolist()
cilindrata_x = df_scalato['cilindrata'].tolist()



prezzo_y_train = prezzo_y[:int((0.8*len(prezzo_y)))]
prezzo_y_test = prezzo_y[int((0.8*len(prezzo_y))):]
cavalli_x_train = cavalli_x[:int(0.8 * len(cavalli_x))]
cavalli_x_test = cavalli_x[int(0.8 * len(cavalli_x)):]

print(predittore(cavalli_x_train, prezzo_y_train, cavalli_x_test))

potenza_x_train = potenza_x[:int(0.8 * len(potenza_x))]
potenza_x_test = potenza_x[int(0.8 * len(potenza_x)):]

print(predittore(potenza_x_train, prezzo_y_train, potenza_x_test))

consumi_x_train = consumi_x[:int(0.8 * len(consumi_x))]
consumi_x_test = consumi_x[int(0.8 * len(consumi_x)):]

print(predittore(consumi_x_train, prezzo_y_train, consumi_x_test))

emissioni_x_train = emissioni_x[:int(0.8 * len(emissioni_x))]
emissioni_x_test = emissioni_x[int(0.8 * len(emissioni_x)):]

print(predittore(emissioni_x_train, prezzo_y_train, emissioni_x_test))

serbatoio_x_train = serbatoio_x[:int(0.8 * len(serbatoio_x))]
serbatoio_x_test = serbatoio_x[int(0.8 * len(serbatoio_x)):]

print(predittore(serbatoio_x_train, prezzo_y_train, serbatoio_x_test))

cilindrata_x_train = cilindrata_x[:int(0.8 * len(cilindrata_x))]
cilindrata_x_test = cilindrata_x[int(0.8 * len(cilindrata_x)):]

print(predittore(cilindrata_x_train, prezzo_y_train, cilindrata_x_test))
