from decimal import Decimal
from api import *
import os
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



@app.route('/chisiamo')
def chisiamo():
   return render_template('ChiSiamo.html')


if __name__ == '__main__':
    app.run(debug=True)