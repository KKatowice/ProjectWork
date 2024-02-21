import json
import re
import pandas as pd
from tqdm import tqdm
import copy

def dai():
    with open('completo_wPrices.json', 'r') as f:
        dcarModel = json.load(f)
        dcarModel_cln = copy.deepcopy(dcarModel)
        deletatiByCilindr = 0
        deletatiByEng = 0
        for brand in tqdm(dcarModel.keys()):
            for model in dcarModel[brand].keys():
                if model == 'imglink': continue
                a = dcarModel[brand][model]
                if a['price'] < 1000:
                    dcarModel_cln[brand][model]['price'] = None
                for eng in a['engines'].keys():
                    if len(a['engines'][eng].keys()) <3:
                        print("cancello [eng < 3]",brand, model, eng)
                        del dcarModel_cln[brand][model]['engines'][eng]
                        deletatiByEng += 1

                    disp = a['engines'][eng].get('Displacement:')
                    pdisp = a['engines'][eng].get('Pdisplacement')
                    if disp == None and pdisp == None:
                        print("cancello [no cilindr info]",brand, model, eng)
                        del dcarModel_cln[brand][model]['engines'][eng]
                        deletatiByCilindr += 1
                    elif pdisp == None and disp:
                        #print('DIIIIS', int(disp.split()[0])/1000)
                        dcarModel_cln[brand][model]['engines'][eng]['Pdisplacement:'] = f"{int(disp.split()[0])/1000}L"
        print("cancellatiByEng", deletatiByEng)
        print("cancellatiByCilindr", deletatiByCilindr)
                    
    with open('completo_wPrices_cleaner.json', 'w') as f:
        json.dump(dcarModel_cln, f)
            
dai()