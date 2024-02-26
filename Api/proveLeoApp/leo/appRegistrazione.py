from decimal import Decimal
from urllib import request
from flask import *
from api import *
import os
import secrets
from flask_mail import Mail, Message
from werkzeug import check_password_hash
""" cwd = os.getcwd()
print(cwd) """

#app = Flask(__name__)
app.register_blueprint(apiBlueprint)

DBNAME = "concessionario"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('ID')}:{os.getenv('PSW')}@"
    f"{os.getenv('H')}:{os.getenv('PRT')}/concessionario"
)




app = Flask(__name__)

# Configura i dettagli per il servizio SMTP
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'daita12projectwork@outlook.it'
app.config['MAIL_PASSWORD'] = os.getenv('password')
app.config['MAIL_DEFAULT_SENDER'] = 'daita12projectwork@outlook.it'

mail = Mail(app)

# Database fittizio per archiviare i token di conferma
confirmation_tokens = {}


# Pagina di registrazione
@app.route('/crea_account', methods=['GET', 'POST'])
def register():
    connessione = create_db_connection(DBNAME)
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        eta = request.form['eta']
        sesso = request.form['sesso']
        email = request.form['email']
        password = request.form['password']
        provincia = request.form['provincia']
        q = f""" SELECT * FROM utente WHERE nome= '{nome}' AND  cognome = '{cognome}' AND eta= '{eta}' AND sesso = '{sesso}' AND email = '{email}' AND password = '{password}' AND provincia = '{provincia}');"""
        verifica = read_query(connessione, q)

        if len(verifica) == 0:
            token = secrets.token_urlsafe(16)
            confirmation_tokens[token] = email
            send_confirmation_email(email, token)
            q1 = f"""INSERT INTO utente(nome, cognome, eta, sesso, email, password, provincia)
                             VALUES('{nome}','{cognome}','{eta}','{sesso}','{email}','{password}','{provincia}')"""
            execute_query(connessione,q1)
            connessione.close()
            return {'success': True}

        else:
            return {'success': False}
    else:
        return render_template("crea_account.html")


# Pagina di conferma registrazione
@app.route('/registration_confirmation')
def registration_confirmation():
    return render_template('registration_confirmation.html')


# Pagina di conferma registrazione con token
@app.route('/confirm_registration/<token>')
def confirm_registration(token):
    connessione = create_db_connection(DBNAME)
    email = confirmation_tokens.get(token)
    if email:
        # Attiva l'account dell'utente nel database
        del confirmation_tokens[token]  # Rimuovi il token dopo la conferma
        q1 = f"""UPDATE utenti SET(registrazione =True) WHERE email = '{email}'"""
        execute_query(connessione, q1)
        connessione.close()
        return render_template("'registration_success.html")


    else:
        return 'Token di conferma non valido.'


# Funzione per inviare l'email di conferma
def send_confirmation_email(email, token):
    message = Message(subject='Conferma registrazione',
                      recipients=[email],
                      html=f'Clicca <a href="{url_for("http://127.0.0.1:5000/confirm_registration", token=token, _external=True)}">qui</a> per confermare la registrazione.')
    mail.send(message)


if __name__ == '__main__':
    app.run(debug=True)

