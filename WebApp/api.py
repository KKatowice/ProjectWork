from classAuto import *
from sys import path

isFABIO = False
if not isFABIO:
    path.append(r'ProjectWork/Database')
    from ProjectWork.Database.dbUtils_aiven import *
else:
    path.append(r'Database')
    from dbUtils_aiven import *

apiBlueprint = Blueprint("apiBlueprint", __name__)

DBNAME = "concessionario"


# --auto--
@apiBlueprint.route('/api/getAuto', methods=['GET'])
def getAuto():
    page = int(request.args.get('page', default=1))
    items_per_page = 42
    offset = (page - 1) * items_per_page
    c = create_db_connection(DBNAME)


    q = f"""SELECT * FROM auto
         JOIN motori ON motori.id_motore = auto.id_motore
         JOIN marchi ON marchi.id_marchio = auto.id_marchio
         ORDER BY auto.prezzo
         LIMIT {items_per_page} OFFSET {offset};"""

    res = read_query(c, q)
    c.close()
    return res

@apiBlueprint.route('/api/getMarchio', methods=['GET'])
def getMarchio():
    page = int(request.args.get('page', default=1))
    items_per_page = 21
    offset = (page - 1) * items_per_page
    c = create_db_connection(DBNAME)

    q = f"""SELECT * FROM marchi
         ORDER BY marchi.nome
         LIMIT {items_per_page} OFFSET {offset};"""

    res = read_query(c, q)
    c.close()
    return res

@apiBlueprint.route('/api/getAutobyMarchio', methods=['GET'])
def getAutobyMarchio():
    marchio = request.args.get('marchio')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN marchi ON auto.id_marchio = marchi.id_marchio 
        JOIN motori ON auto.id_motore = motori.id_motore WHERE marchi.nome = '{marchio}'; """
    res = read_query(c, q)
    c.close()
    return res

# --tutte le auto per motore--
@apiBlueprint.route('/api/getAutobyMotori', methods=['GET'])
def getAutobyMotori():
    cilindratamax = request.args.get('cilindratamax')
    cilindratamin = request.args.get('cilindratamin')
    c = create_db_connection("concessionario")
    q = f"""SELECT * FROM auto JOIN motori ON auto.id_motore = motori.id_motore WHERE motore.cilindrata BETWEEN '{cilindratamin}' AND '{cilindratamax}'; """
    res = read_query(c, q)
    c.close()
    return res

# @apiBlueprint.route('/api/get', methods=['GET'])
# def Top10Film():
#     c = create_db_connection(DBNAME)
#     q = "SELECT * FROM film ORDER BY Average_rating DESC LIMIT 10"
#     res = read_query(c, q)
#     c.close()
#     return res




# --CRUD--
# datetime formato pe date: 'YYYY-MM-DD HH:MM:SS'

@apiBlueprint.route('/api/getRicerca', methods=['GET'])
def getRicerca():
    form_data = request.form
    # Estrai i dati dal form
    cilindrata = form_data.get('cilindrata')
    marca = form_data.get('marchio')
    capacità_serbatoio = form_data("capacità_serbatoio")

    # Esegui la ricerca nel database basata sui dati del form
    c = create_db_connection(DBNAME)
    q = f"""SELECT * FROM auto
        JOIN motori ON motori.id_motore = auto.motori
        JOIN marchi ON marchi.id_marchio = auto.id_marchio 
        WHERE motori.cilindrata = '{cilindrata}' AND marchi.nome = '{marca}'; """
    res = read_query(c, q)
    c.close()

    # Restituisci i risultati alla pagina web
    return render_template('risultati_ricerca.html', risultati=res)

# --PAGINA UTENTE--
@apiBlueprint.route('/api/getAutobyBudget', methods=['GET'])
def getAutobyBudget():
    num_utente = request.args.get("num_utente")
    c = create_db_connection("concessionario")
    q1 = f"""SELECT budget FROM utente WHERE id_utente = "{num_utente}"; """
    budget = read_query(c, q1)[0]['budget']
    q2 = f"""SELECT * FROM auto
         JOIN motori ON motori.id_motore = auto.id_motore
         JOIN marchi ON marchi.id_marchio = auto.id_,marchio
         WHERE auto.prezzo < {budget};"""

    res = read_query(c, q2)
    c.close()
    return res


@apiBlueprint.route('/api/auto_filter', methods=['POST'])
def filtra_auto():
    from classAuto import Auto, Motore, Marchio
    data = request.get_json()
    print(data)
    markio = data.get('marchio')
    print(markio)
    q = (Auto.query.join(Motore, Motore.id_motore == Auto.id_motore).join(Marchio, Marchio.id_marchio == Auto.id_marchio).filter(Marchio.nome == data['marchio']).filter(Motore.carburante == data['carburante']).filter(Motore.consumi < float(data['consumi'])).filter(Motore.emissioni < float(data['emissioni'])).filter(Auto.prezzo < float(data['prezzo'])).filter(Motore.serbatoio > float(data['serbatoio'])).filter(Motore.potenza > int(data['potenza'])).filter(Motore.cilindrata > int(data['cilindrata'])).filter(Motore.cavalli > int(data['cavalli'])))
    print("success")
    result = q.all()
    print("success")
    return result



