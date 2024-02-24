import csv
from random import randint
from faker import Faker
import json
import random
import string

lista_province= []
with open("caprovince.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)
    for elem in reader:
        lista_province.append(elem[0])

print(lista_province)

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
    eta =(randint(18,110))
    budget =(randint(15_000,300_000))
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

