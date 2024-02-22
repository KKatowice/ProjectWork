from api import *
import os
import requests

app = Flask(__name__)
app.register_blueprint(apiBlueprint)

DBNAME = "concessionario"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('ID')}:{os.getenv('PSW')}@"
    f"{os.getenv('H')}:3306/concessionario"
)

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/auto', methods=['GET', 'POST'])
def show_auto():
    api_url = 'http://127.0.0.1:5000/api/auto_filter'
    response = requests.get(api_url)

    page = int(request.args.get('page', default=1))
    items_per_page = 20
    c = create_db_connection("concessionario")
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    if response.status_code == 200:
        data = filtra_auto()
        print(data)
        if len(data) > 0:
            lista_auto = [x.to_dict() for x in data]
        else:
            lista_auto = []
            print('risotto')
    else:
        lista_auto = getAuto()
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
    return render_template('auto_x_marchio.html', auto=auto)


if __name__ == '__main__':
    app.run(debug=True)