import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import KNeighborsRegressor

from ProjectWork.Database.dbUtils_aiven import *

c = create_db_connection(DBNAME)
q = """SELECT auto.prezzo, marchi.nome, motori.carburante, motori.cavalli, motori.cilindrata,
    motori.consumi, motori.emissioni, motori.potenza, motori.serbatoio
    FROM auto JOIN marchi JOIN motori
    ON auto.id_marchio = marchi.id_marchio AND auto.id_motore = motori.id_motore;"""
ldd = read_query(c, q)
# Caricamento del dataset
data = pd.DataFrame(ldd)  # Sostituisci con il percorso del tuo dataset
# for x in data.columns:
#     print(x)

# print(data.head())
df_selected_columns_loc = data.loc[:, ['cavalli', 'potenza', 'prezzo']]
c = df_selected_columns_loc.columns
# data = data.dropna()
scaler = StandardScaler()
data = scaler.fit_transform(df_selected_columns_loc)
data = pd.DataFrame(data, columns=c)



# Dividi il dataset in variabili indipendenti (predictors) e variabile dipendente (target)
X = data[['cavalli', 'potenza']]  # Seleziona le colonne del dataset che vuoi utilizzare come predittori
y = data['prezzo']  # Seleziona la colonna del dataset che rappresenta la temperatura

# Divisione del dataset in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creazione del modello di regressione lineare
model = LinearRegression()

# Addestramento del modello sul set di addestramento
model.fit(X_train, y_train)

# Predizione della temperatura sul set di test
y_pred = model.predict(X_test)

# Valutazione delle prestazioni del modello
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("Coefficient of Determination (R^2):", r2)

correlation_matrix = df_selected_columns_loc.corr()

# Stampa della heatmap della correlazione
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap della Correlazione')
plt.show()



model = KNeighborsRegressor(n_neighbors=2)
model.fit(X_train,y_train)
preds=model.predict(X_test)
print(r2_score(preds,y_test))



