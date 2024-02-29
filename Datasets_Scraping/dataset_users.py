import csv
from random import randint
from faker import Faker
import json
import random
import string

# lista_province= []
# with open("caprovince.csv", "r", encoding="utf-8") as file:
#     reader = csv.reader(file, delimiter=";")
#     next(reader)
#     for elem in reader:
#         lista_province.append(elem[0])
#
# print(lista_province)

lista_province = ['Agrigento', 'Alessandria', 'Ancona', 'Bari',
                  'Bergamo', 'Biella', 'Bologna', 'Brescia',
                  'Brindisi', 'Cagliari', 'Caltanissetta', 'Catania',
                  'Chieti', 'Cuneo', 'Enna', 'Firenze',
                  'Frosinone', 'Genova', 'Isernia', 'Lecce',
                  'Livorno', 'Milano', 'Napoli', 'Novara', 'Nuoro',
                  'Olbia-Tempio', 'Oristano','Reggio di Calabria', "Reggio nell'Emilia",
                  'Roma', 'Salerno', 'Siracusa', 'Torino', 'Trapani', 'Trento']


d = {}
sessi = ['maschio', 'femmina', 'altro']
fake = Faker()

lista=[]
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
password = generate_random_password()
print(password)

for x in range(1,10_000):
    email = (fake.email())
    while email in lista:
        email = (fake.email())
    lista.append(email)
    stringa =fake.name().split(" ")
    password = generate_random_password()
    nome = stringa[0]
    cognome = stringa[1]
    provincia= random.choice(lista_province)
    eta =(randint(18,100))
    if eta >= 18 and eta < 23:
        budget =(randint(10_000,20_000))
    elif eta >=23  and eta < 28:
        budget =(randint(20_000,50_000))
    elif eta >=28 and eta < 35:
        budget =(randint(30_000,100_000))
    elif eta >=35 and eta < 55:
        budget =(randint(60_000,200_000))
    elif eta >=55 and eta < 75:
        budget =(randint(50_000,200_000))
    elif eta > 75:
        budget =(randint(100_000,250_000))
    sesso = sessi[randint(0,2)]

    d[x] = {'nome': nome,
            'cognome': cognome,
            'eta':eta,
            'sesso': sesso,
            'email': email,
            'password': password,
            'provincia': provincia,
            'budget': budget
            }

with open('utenti_official.json', 'w') as f:
    json.dump(d, f)

