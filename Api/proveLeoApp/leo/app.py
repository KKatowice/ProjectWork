from flask import *

from WebApp.api import getMarchio
from api import *


app = Flask(__name__)
app.register_blueprint(apiBlueprint)
DBNAME = "concessionario"

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/auto')
def show_auto():
    param_ord = request.args.get('param_ord')
    page = int(request.args.get('page', default=1))
    items_per_page = 20
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    marchi = request.args.get('marchi', default=None)

    if marchi:
        if isinstance(marchi, str):
            data = getAutobyMarchio()
        else:
            raise TypeError("L'auto deve essere una stringa")
    else:
        if param_ord == "dal più basso":
            data = getAuto(param_ord='asc')
        elif param_ord == "dal più alto":
            data = getAuto(param_ord='desc')
        else:
            data = getAuto()

    c.close()
    return render_template('auto.html', auto=data, page=page, total_pages=totale)



@app.route('/marchi')
def show_marchi():
    page = int(request.args.get('page', default=1))
    items_per_page = 10
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_marchi FROM marchi"
    conteggio = read_query(c, query)[0]['num_marchi']
    totale = (conteggio // items_per_page) + 1
    data = getMarchio()
    return render_template('marchi.html', generi=data, page=page, total_pages=totale)

@app.route('/login', methods=['GET', 'POST'])
def login():
    connessione = create_db_connection(DBNAME)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        q1 = f"""SELECT email,password FROM utente WHERE {email} AND {password}"""
        verifica = execute_query(connessione, q1)
        if len(verifica) > 1:        # Password corretta, autenticazione riuscita
            return redirect(url_for('dashboard'))
        else:
            return "email o password errate"
        # else:
        #     # Password errata, incrementa il numero di tentativi
        #     attempts += 1
        #     remaining_attempts = max_attempts - attempts
        #     if remaining_attempts > 0:
        #         return f"Password errata. {remaining_attempts} tentativi rimanenti."
        #     else:
        #         c.execute("INSERT INTO utenti_bloccati (email) VALUES (?)", (email,))
        #         conn.commit()

    else:
        return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def register():
    connessione = create_db_connection(DBNAME)
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        eta = request.form['eta']
        sesso = request.form['sesso']
        email = request.form['email']
        password = request.form['password']
        cap = request.form['cap']
        q = f"""INSERT INTO utente(nome, cognome, eta, sesso, email, password, cap)
                             VALUES({nome},{cognome},{eta},{sesso},{email},{password},{cap})"""
        verifica = read_query(connessione, q)

        if len(verifica) == 0:
            execute_query(connessione, q)

        else:
            return "mail già utilizzata"
    else:
        return render_template("register.html")









if __name__ == '__main__':
   app.run(debug=True)
