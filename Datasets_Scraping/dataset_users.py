from faker import Faker
from random import randint
from faker import Faker
import json


d = {}
sessi = ['maschio', 'femmina', 'altro']
fake = Faker()

lista=[]

for x in range(1,10_000):
    email = (fake.email())
    while email in lista:
        email = (fake.email())
    lista.append(email)
    stringa =fake.name().split(" ")
    nome = stringa[0]
    cognome = stringa[1]
    cap= (fake.zipcode())
    eta =(randint(18,110))
    budget =(randint(15_000,300_000))
    sesso = sessi[randint(0,2)]
    d[x] = {'nome': nome,
            'cognome': cognome,
            'eta':eta,
            'sesso': sesso,
            'email': email,
            'cap': cap,
            'budget': budget
            }

with open('utenti.json', 'w') as f:
    json.dump(d, f)

