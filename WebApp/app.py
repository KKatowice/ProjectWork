from decimal import Decimal

import requests
from flask_mail import Mail, Message
from werkzeug.security import *
import secrets
from api import *
import os
""" cwd = os.getcwd()
print(cwd) """

#app = Flask(__name__)
app.register_blueprint(apiBlueprint)
app.secret_key = 'VERY_BAD_SECRET_KEY'
DBNAME = "concessionario"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('ID')}:{os.getenv('PSW')}@"
    f"{os.getenv('H')}:{os.getenv('PRT')}/concessionario"
)

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'daita12projectwork@outlook.it'
app.config['MAIL_PASSWORD'] = os.getenv('password')
app.config['MAIL_DEFAULT_SENDER'] = 'daita12projectwork@outlook.it'

mail = Mail(app)

def send_confirmation_email(email, token):
    print(token)
    message = Message(subject='Conferma registrazione',
                      recipients=[email],
                      html=f'Clicca <a href="http://127.0.0.1:5000/confirm_registration?token={token}">qui</a> per confermare la registrazione.')

    print(message)
    mail.send(message)
@app.route('/')
def home():
   return render_template('Home.html')

@app.route('/grafici')
def grafs():
   return render_template('Grafici.html')


@app.route('/auto', methods=['GET'])
def show_auto():

    f = request.args.get('filtro', default=None)
    page = int(request.args.get('page', default=1))
    items_per_page = 42
    c = create_db_connection("concessionario")
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    if f == 'filtrate':
        #                callzLink = `/auto?filtro=filtrate&marchio=${marchio}&carburante=${carburante}&consumi=${consumi}&emissioni=${emissioni}&prezzo=${prezzo}&serbatoio=${serbatoio}&potenza=${potenza}&cilindrata=${cilindrata}&cavalli=${cavalli}`
        dd = {
            'marchio': request.args.get('marchio'),
            'carburante': request.args.get('carburante'),
            'consumi': request.args.get('consumi'),
            'emissioni': request.args.get('emissioni'),
            'prezzo': request.args.get('prezzo'),
            'serbatoio': request.args.get('serbatoio'),
            'potenza': request.args.get('potenza'),
            'cilindrata': request.args.get('cilindrata'),
            'cavalli': request.args.get('cavalli')
        }
        print("filtrate", dd)
        data = json.loads(filtra_auto(dd))['data']
        print("ress call!!!!!!!!!!!!!!!!!!!!", data, type(data))
        if len(data) > 0 and type(data) == list:
            lista_auto = data
        else:
            lista_auto = []
        print("passati if else", lista_auto)
    else:
        lista_auto = getAuto()
    for d in lista_auto:
        for key, value in d.items():
            if isinstance(value, Decimal):
                d[key] = float(value)
    print(lista_auto, "fine show_auto, now render template diopan")
    c.close()
    return render_template('Tutte_le_auto.html', auto=lista_auto, page=page, total_pages=totale)

@app.route('/marchi')
def show_marchi():
    page = int(request.args.get('page', default=1))
    items_per_page = 21
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_marchi FROM marchi"
    conteggio = read_query(c, query)[0]['num_marchi']
    totale = (conteggio // items_per_page) + 1
    marchi = getMarchio()
    c.close()
    return render_template('marchi.html', marchi=marchi, page=page, total_pages=totale)

@app.route('/autopermarchio')
def show_auto_for_marchi():
    marchio = request.args.get('marchio')
    if marchio:
        auto = getAutobyMarchio()
    else:
        auto = getAuto()
    for d in auto:
        for key, value in d.items():
            if isinstance(value, Decimal):
                d[key] = float(value)
    return render_template('auto_x_marchio.html', auto=auto)




@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session['utente'] = None
    return redirect('/')
@app.route('/Utente')
def logutente():
    return render_template('Utente.html')

@app.route('/preferiti')
def preferiti():
    mail_utente = session.get('utente')
    lista_auto = getPreferenze(mail_utente)
    for d in lista_auto:
        for key, value in d.items():
            if isinstance(value, Decimal):
                d[key] = float(value)
    return render_template('preferiti.html', auto=lista_auto)


@app.route('/Utente', methods=['GET', 'POST'])
def login():
    connessione = create_db_connection(DBNAME)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        q1 = f"""SELECT email,password FROM utenti WHERE {email} AND {password}"""
        verifica = execute_query(connessione, q1)
        if len(verifica) > 1:        # Password corretta, autenticazione riuscita
            return redirect(url_for('dashboard'))
        else:
            return "email o password errate"
        # else:
            # Password errata, incrementa il numero di tentativi
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                return f"Password errata. {remaining_attempts} tentativi rimanenti."
            else:
                c.execute("INSERT INTO utenti_bloccati (email) VALUES (?)", (email,))
                conn.commit()

    else:
        return render_template('Utente.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f"Benvenuto, {session['email']}! Questa è la tua dashboard."
    else:
        return redirect(url_for('login'))

@app.route('/chisiamo')
def chisiamo():
   return render_template('ChiSiamo.html')

@app.route('/crea_account')
def reg():
   return render_template('crea_account.html')











# Database fittizio per archiviare i token di conferma
confirmation_tokens = {}


# Pagina di registrazione
@app.route('/crea_account', methods=['GET', 'POST'])
def register():
    connessione = create_db_connection(DBNAME)
    if request.method == 'POST':
        data = request.get_json()
        nome = data['nome']
        cognome = data['cognome']
        eta = data['eta']
        sesso = data['sesso']
        email = data['email']
        password = data['password']
        provincia = data['provincia']
        q = f""" SELECT * FROM utenti WHERE nome= '{nome}' AND  cognome = '{cognome}' AND eta= '{eta}' AND sesso = '{sesso}' AND email = '{email}' AND password = '{password}' AND provincia = '{provincia}');"""
        verifica = read_query(connessione, q)

        if verifica == None:
            token = secrets.token_urlsafe(16)
            confirmation_tokens[token] = email
            send_confirmation_email(email, token)
            q1 = f"""INSERT INTO utenti(nome, cognome, eta, sesso, email, password, provincia)
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
@app.route('/confirm_registration')
def confirm_registration():
    token = request.args.get('token')
    connessione = create_db_connection(DBNAME)
    email = confirmation_tokens.get(token)
    if email:
        # Attiva l'account dell'utente nel database
          # Rimuovi il token dopo la conferma
        q1 = f"""UPDATE utenti SET registrazione = 1 WHERE email = '{email}'"""
        execute_query(connessione, q1)
        connessione.close()
        del confirmation_tokens[token]
        return render_template("'registration_success.html")


    else:
        return 'Token di conferma non valido.'


# Funzione per inviare l'email di conferma

@app.route('/search', methods= ['GET'])
def search():
    name = request.args.get('name')
    results = Auto.query.join(Motore, Motore.id_motore == Auto.id_motore).join(Marchio, Marchio.id_marchio == Auto.id_marchio).with_entities(Auto, Motore, Marchio).filter(Auto.modello.ilike(f'%{name}%')).all()
    print(results)
    result_data = []
    for t in results:
        a = t[0].to_dict()
        b = t[1].to_dict()
        c = t[2].to_dict()
        dd = a | b | c
        print(dd)
        result_data.append(dd)
    print(result_data)
    for d in result_data:
        for key, value in d.items():
            if isinstance(value, Decimal):
                d[key] = float(value)
    return render_template('search.html', auto=result_data)

if __name__ == '__main__':
    app.run(debug=True)