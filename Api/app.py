from flask import Flask, render_template, request
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
    auto = request.args.get('auto', default=None)
    if auto:
        if isinstance(auto, str):
            data = getAuto()
        else:
            raise TypeError("l'auto deve essere una stringa")
    else:
        data = getAuto()
        if param_ord == "dal p":
            data = data.sort(lambda x: x["Title"])
        elif param_ord == "4_stelle":
            data = get_evaluation()
    top_diesci = Top10Film()
    return render_template('auto.html', auto=data, page=page, total_pages=totale)


@app.route('/marchi')
def show_generi():
    page = int(request.args.get('page', default=1))
    items_per_page = 10
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_generi FROM generi"
    conteggio = read_query(c, query)[0]['num_generi']
    totale = (conteggio // items_per_page) + 1
    data = getGeneri()
    return render_template('Generi.html', generi=data, page=page, total_pages=totale)

# @app.route('/grafici')
# def showGrafici():
#     return render_template('Grafici.html')



if __name__ == '__main__':
   app.run(debug=True)
