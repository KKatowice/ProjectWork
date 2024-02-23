
from werkzeug.security import generate_password_hash,check_password_hash


password = 'Gaiaèlamiacrushdelliceo69'
a = generate_password_hash(password)
b = len(generate_password_hash(password))
print(b)
c = check_password_hash(a, password)
print(c)