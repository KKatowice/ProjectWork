from flask import Flask, render_template, request
from api import *


app = Flask(__name__)
app.register_blueprint(apiBlueprint)
DBNAME = "concessionario"

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/auto')
def show_film():
    param_ord = request.args.get('param_ord')
    page = int(request.args.get('page', default=1))
    items_per_page = 20
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_film FROM film"
    conteggio = read_query(c, query)[0]['num_film']
    totale = (conteggio // items_per_page) + 1
    genere = request.args.get('genere', default=None)
    if genere:
        if isinstance(genere, str):
            data = getMovieByGenre()
        else:
            raise TypeError("Il genere deve essere una stringa")
    else:
        data = getMovies()
        if param_ord == "az":
            data = data.sort(lambda x: x["Title"])
        elif param_ord == "4_stelle":
            data = get_evaluation()
    top_diesci = Top10Film()
    return render_template('Film.html', films=data, topdieci=top_diesci, page=page, total_pages=totale)


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
