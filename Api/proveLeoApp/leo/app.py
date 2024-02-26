from decimal import Decimal
from api import *
import os
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



@app.route('/')
def home():
   return render_template('Home.html')


@app.route('/auto', methods=['GET', 'POST'])
def show_auto():
    f = request.args.get('filtro', default=None)
    page = int(request.args.get('page', default=1))
    items_per_page = 42
    c = create_db_connection("concessionario")
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    if f == 'filtrate':
        print(f)
        data = filtra_auto()
        print("dataz ",data)
        if len(data) > 0:
            lista_auto = [x.to_dict() for x in data]
        else:
            lista_auto = []
    else:
        lista_auto = getAuto()
    for d in lista_auto:
        for key, value in d.items():
            if isinstance(value, Decimal):
                d[key] = float(value)
    print(lista_auto)
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

@app.route('/validateLogin', methods=['POST'])

def validateLogin():
    connessione = create_db_connection(DBNAME)
    try:
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        q = f"""SELECT password FROM utenti WHERE email = {email}"""
        data = read_query(connessione,q)[0]

        if len(data) > 0:
            if check_password_hash(str(data['password']), password):
                # session['utente'] = data[0][0]
                return redirect('/')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        connessione.close()


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


# @app.route('/Utente', methods=['GET', 'POST'])
# def login():
#     connessione = create_db_connection(DBNAME)
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         q1 = f"""SELECT email,password FROM utenti WHERE {email} AND {password}"""
#         verifica = execute_query(connessione, q1)
#         if len(verifica) > 1:        # Password corretta, autenticazione riuscita
#             return redirect(url_for('dashboard'))
#         else:
#             return "email o password errate"
        # else:
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


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = chatbot.respond(user_message)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)