
from werkzeug.security import generate_password_hash,check_password_hash


password = 'admin'
a = generate_password_hash(password)
print(a)