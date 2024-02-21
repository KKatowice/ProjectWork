from flask import *
from Database.creazioneDatabase import utenti
from provaApi import *
import sqlite3
# from ProjectWork.Database.dbUtils import create_db_connection, read_query

app = Flask(__name__)
app.register_blueprint(apiBlueprint)
DBNAME = "concessionario"
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('ID')}:{os.getenv('PSW')}@"
    f"{os.getenv('H')}:3306/concessionario"
)

def select_specific_instance(table_name, instance_id):
    c = create_db_connection(DBNAME)
    query = f"SELECT * FROM {table_name} WHERE id = ?;"
    result = read_query(c, query, (instance_id,))
    c.close()
    return result

@app.route('/')
def home():
   return render_template('home.html')



@app.route('/auto')
def show_auto():
    f = request.args.get('filtro', default=None)
    page = int(request.args.get('page', default=1))
    items_per_page = 20
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    if f:
        data = filtra_auto()
        if len(data) > 0:
            lista_auto = [x.to_dict() for x in data]
        else:
            lista_auto = []
    else:
        lista_auto = getAuto()
    c.close()
    return render_template('Tutte_le_auto.html', auto=lista_auto, page=page, total_pages=totale)



@app.route('/marchi')
def show_marchi():
    page = int(request.args.get('page', default=1))
    items_per_page = 10
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_marchi FROM marchi"
    conteggio = read_query(c, query)[0]['num_marchi']
    totale = (conteggio // items_per_page) + 1
    marchi = getMarchio()
    return render_template('marchi.html', marchi=marchi, page=page, total_pages=totale)

@app.route('/marchi/autoByMarchio')
def show_autoByMarchio():
    page = int(request.args.get('page', default=1))
    items_per_page = 10
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_marchi FROM marchi"
    conteggio = read_query(c, query)[0]['num_marchi']
    totale = (conteggio // items_per_page) + 1
    data = getAutobyMarchio()
    return render_template('auto_x_marchio.html', marchi=data, page=page, total_pages=totale)

conn = sqlite3.connect('users.db')
c = conn.cursor()
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in utenti:
            # Controllo sul numero massimo di tentativi
            max_attempts = 3
            attempts = 0
            while attempts < max_attempts:
                if password == utenti[email]:
                    # Password corretta, autenticazione riuscita
                    return redirect(url_for('dashboard'))
                else:
                    # Password errata, incrementa il numero di tentativi
                    attempts += 1
                    remaining_attempts = max_attempts - attempts
                    if remaining_attempts > 0:
                        return f"Password errata. {remaining_attempts} tentativi rimanenti."
                    else:
                        c.execute("INSERT INTO utenti_bloccati (email) VALUES (?)", (email,))
                        conn.commit()
                        return "Hai esaurito tutti i tentativi. Account bloccato per motivi di sicurezza."

        else:
            return "Email non trovata nel database."
        return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f"Benvenuto, {session['email']}! Questa è la tua dashboard."
    else:
        return redirect(url_for('login'))

# @app.route('/grafici')
# def showGrafici():
#     return render_template('Grafici.html')



if __name__ == '__main__':
   app.run(debug=True)
