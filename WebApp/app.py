from decimal import Decimal

# from werkzeug.security import *

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


@app.route('/')
def home():
   return render_template('Home.html')


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
    return render_template('preferiti.html', auto=lista_auto)


# @app.route('/Utente', methods=['GET', 'POST'])
# def login():
#     connessione = create_db_connection(DBNAME)
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         q1 = f"""SELECT email,password FROM utente WHERE {email} AND {password}"""
#         verifica = execute_query(connessione, q1)
#         if len(verifica) > 1:        # Password corretta, autenticazione riuscita
#             return redirect(url_for('dashboard'))
#         else:
#             return "email o password errate"
#         # else:
        #     # Password errata, incrementa il numero di tentativi
        #     attempts += 1
        #     remaining_attempts = max_attempts - attempts
        #     if remaining_attempts > 0:
        #         return f"Password errata. {remaining_attempts} tentativi rimanenti."
        #     else:
        #         c.execute("INSERT INTO utenti_bloccati (email) VALUES (?)", (email,))
        #         conn.commit()

    # else:
    #     return render_template('Utente.html')
# @app.route('/crea_account', methods=['GET', 'POST'])
# def register():
#     connessione = create_db_connection(DBNAME)
#     if request.method == 'POST':
#         nome = request.form['nome']
#         cognome = request.form['cognome']
#         eta = request.form['eta']
#         sesso = request.form['sesso']
#         email = request.form['email']
#         password = request.form['password']
#         CAP = request.form['CAP']
#         q = f"""INSERT INTO utente(nome, cognome, eta, sesso, email, password, CAP)
#                              VALUES('{nome}','{cognome}','{eta}','{sesso}','{email}','{password}','{CAP}')"""
#         verifica = read_query(connessione, q)
#         print(verifica)
#
#         if len(verifica) == 0:
#             execute_query(connessione, q)
#             print(verifica)
#         else:
#             return "mail già utilizzata"
#     else:
#         return render_template("crea_account.html")
#
# @app.route('/dashboard')
# def dashboard():
#     if 'email' in session:
#         return f"Benvenuto, {session['email']}! Questa è la tua dashboard."
#     else:
#         return redirect(url_for('login'))

@app.route('/chisiamo')
def chisiamo():
   return render_template('ChiSiamo.html')

@app.route('/crea_account')
def reg():
   return render_template('crea_account.html')


if __name__ == '__main__':
    app.run(debug=True)