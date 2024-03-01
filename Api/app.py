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


# @app.route('/grafici')
# def showGrafici():
#     return render_template('Grafici.html')



if __name__ == '__main__':
   app.run(debug=True)