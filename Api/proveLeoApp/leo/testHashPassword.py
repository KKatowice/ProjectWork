
from werkzeug.security import generate_password_hash


password = 'Gaiaèlamiacrushdelliceo69'
a = generate_password_hash(password)
print(a)