import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures


df = pd.read_csv('Dati_auto.csv')

# Controlliamo l'eventuale presenza di valori "nan"

df.info()

# Non ci sono valori nan ma alcuni valori numerici sono "object" invece che "int" o "float". Provvediamo a risolvere:

df['prezzo'] = pd.to_numeric(df['prezzo'])
df['cavalli'] = pd.to_numeric(df['cavalli'])
df['cilindrata'] = pd.to_numeric(df['cilindrata'])
df['consumi'] = pd.to_numeric(df['consumi'])
df['emissioni'] = pd.to_numeric(df['emissioni'])
df['potenza'] = pd.to_numeric(df['potenza'])
df['serbatoio'] = pd.to_numeric(df['serbatoio'])

# Restano due campi non numerici che non avranno effetto nel misurare la correlazione con una regressione lineare,
# quindi eliminiamo queste due colonne

df = df.drop(['nome', 'carburante'], axis=1)

# Infine notiamo che i dati hanno unità di misura diverse e scale assai differenti, decidiamo quindi di normalizzarli

colonne = df.columns
scaler = StandardScaler()
data = scaler.fit_transform(df)
df = pd.DataFrame(data, columns=colonne)

# Iniziamo con una serie di scatterplot che mostrino le relazioni tra il prezzo e ciascuna delle altre variabili

fig, axes = plt.subplots(3,3 , figsize=(24,18))
fig.tight_layout(pad=5.0)
axes = axes.flatten()
features = df.columns[1:]
for i in range(len(features)):
    sns.scatterplot(data=df, x=features[i], y="prezzo", ax=axes[i])
    plt.xlabel(str(features[i]))
    plt.ylabel('Prezzo')
# plt.show()

# Notiamo da subito che i dati appaiono abbastanza sparsi e disordinati sul piano. Già da qui possiamo inferire che ci sia un
# basso indice di correlazione, ma ce ne sinceriamo con una heatmap:

correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap della Correlazione')
# plt.show()

# Completare

# Creiamo le variabili target e training e attraverso train_test_split generiamo le variabili per il training del modello e
# quelle per il test

target = df['prezzo']
training = df.drop('prezzo', axis=1)
X_train, X_test, y_train, y_test = train_test_split(training, target, test_size=0.2, random_state=42)

# Ora istanziamo il modello di regressione lineare, lo addestriamo, facciamo delle predizioni e le visualizziamo insieme all'r^2

model = LinearRegression()
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(y_test,preds))

# Osserviamo che otteniamo un r^2 negativo: questo avviene per via del tipo di calcolo effettuato da scikit learn, diverso
# da quello della normale regressione lineare. In ogni caso ci indica, come ci aspettavamo che i dati in nostro possesso
# apparentemente non sono in grado di predire i prezzi delle auto.

# Otteniamo risulati simili anche con altri modelli

# Decision Tree


model = DecisionTreeRegressor()
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(y_test, preds))

# Random Forest


model = RandomForestRegressor()
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(y_test, preds))

# KNeighbors Regressor


model = KNeighborsRegressor(n_neighbors=2)
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(y_test, preds))

# Funzione che prende due liste di training e una di test e restituisce la lista delle predizioni, la correlazione r e il
#coefficiente di determinazione r^2
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
    return [lista_predizioni, r, r_quadro]

# Dal dataframe estraiamo le liste dei prezzi e delle due variabili che correlano maggiormente (cavalli e potenza),
# le splittiamo per ottenere dati di training e dati di test e infine facciamo la regressione lineare

prezzo_y = df['prezzo'].tolist()
cavalli_x = df['cavalli'].tolist()
potenza_x = df['potenza'].tolist()


prezzo_y_train = prezzo_y[:int((0.8*len(prezzo_y)))]
prezzo_y_test = prezzo_y[int((0.8*len(prezzo_y))):]
cavalli_x_train = cavalli_x[:int(0.8 * len(cavalli_x))]
cavalli_x_test = cavalli_x[int(0.8 * len(cavalli_x)):]

print(predittore(cavalli_x_train, prezzo_y_train, cavalli_x_test))

potenza_x_train = potenza_x[:int(0.8 * len(potenza_x))]
potenza_x_test = potenza_x[int(0.8 * len(potenza_x)):]

print(predittore(potenza_x_train, prezzo_y_train, potenza_x_test))

# Sfortunatamente notiamo di nuovo valori fuori scala e una correlazione inesistente.

# Utilizziamo una polinomiale di secondo grado per evitare l'overfitting

poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(training)
X_train, X_test, y_train, y_test = train_test_split(poly_features, target, test_size=0.2, random_state=42)
poly_reg_model = LinearRegression()
poly_reg_model.fit(X_train, y_train)
print(poly_reg_model.coef_)
print(poly_reg_model.intercept_)
poly_reg_y_predicted = poly_reg_model.predict(X_test)
print(r2_score(y_test, poly_reg_y_predicted))

# training = np.reshape(df['potenza'],(3004, 1))
#
# poly = PolynomialFeatures(degree=2, include_bias=False)
# poly_features = poly.fit_transform(training)
# X_train, X_test, y_train, y_test = train_test_split(poly_features, target, test_size=0.2, random_state=42)
# poly_reg_model = LinearRegression()
# poly_reg_model.fit(X_train, y_train)
#
# poly_reg_y_predicted = poly_reg_model.predict(X_test)
# print(r2_score(y_test, poly_reg_y_predicted))
