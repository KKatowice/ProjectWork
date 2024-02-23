import os
import sys
#cw = os.getcwd()

@apiBlueprint.route('/api/auto_filter', methods=['GET', 'POST'])
def filtra_auto():
    from classAuto import Auto, Motore, Marchio
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        q = (Auto.query.join(Motore, Motore.id_motore == Auto.id_motore)
             .join(Marchio, Marchio.id_marchio == Auto.id_marchio)
             .filter(Marchio.nome == data['marchio'])
             .filter(Motore.carburante == data['carburante'])
             .filter(Motore.consumi < float(data['consumi']))
             .filter(Motore.emissioni < float(data['emissioni']))
             .filter(Auto.prezzo < float(data['prezzo']))
             .filter(Motore.serbatoio > float(data['serbatoio']))
             .filter(Motore.potenza > int(data['potenza']))
             .filter(Motore.cilindrata > int(data['cilindrata']))
             .filter(Motore.cavalli > int(data['cavalli'])))
        print("success")
        result = q.all()
        print("success")
        print(result)
    else:
        l = []
        return l