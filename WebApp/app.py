
from ..Api.api import *
from flask import Flask, render_template, request

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/auto')
def show_auto():

    page = int(request.args.get('page', default=1))
    items_per_page = 20
    c = create_db_connection(DBNAME)
    query = "SELECT COUNT(*) AS num_auto FROM auto"
    conteggio = read_query(c, query)[0]['num_auto']
    totale = (conteggio // items_per_page) + 1
    marchi = request.args.get('marchio', default=None)

    if marchi:
        if isinstance(marchi, str):
            data = getAutobyMarchio()
        else:
            raise TypeError("L'auto deve essere una stringa")
    else:
        data=getAuto()

    c.close()
    return render_template('auto.html', auto=data, page=page, total_pages=totale)