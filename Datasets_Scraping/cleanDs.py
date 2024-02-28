import json
import re
import pandas as pd
from tqdm import tqdm
import copy

isFabio = True
if isFabio == False:
    chrome_driver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    pathFile = "completo_wPrices_cleaner_official.json"
    pathInitFile = "completo_wPrices_official.json"
else:
    chrome_driver_path = "/usr/bin/google-chrome"
    pathFile = "Datasets_Scraping/completo_wPrices_cleaner_official.json"
    pathInitFile = "Datasets_Scraping/completo_wPrices_official.json"




def dai():
    with open(pathInitFile, 'r') as f:
        dcarModel = json.load(f)
        dcarModel_cln = copy.deepcopy(dcarModel)
        deletatiByCilindr = 0
        deletatiByEng = 0
        for brand in tqdm(dcarModel.keys()):
            for model in dcarModel[brand].keys():
                if model == 'imglink': continue
                a = dcarModel[brand][model]
                """ if a['price'] < 1000:
                    dcarModel_cln[brand][model]['price'] = None """
                if a['price'] == 0:
                    del dcarModel_cln[brand][model]
                    continue
                
                if len(a['engines'].keys()) == 0:
                    print("cancello [eng == 0]",brand, model)
                    del dcarModel_cln[brand][model]
                    deletatiByEng += 1
                    continue
                for eng in a['engines'].keys():
                    if len(a['engines'][eng].keys()) <3:
                        print("cancello [eng < 3]",brand, model, eng)
                        del dcarModel_cln[brand][model]['engines'][eng]
                        deletatiByEng += 1
                        continue
                
                    disp = a['engines'][eng].get('Displacement:')
                    pdisp = a['engines'][eng].get('Pdisplacement')
                    if disp == None and pdisp == None:
                        print("cancello [no cilindr info]",brand, model, eng)
                        del dcarModel_cln[brand][model]['engines'][eng]
                        deletatiByCilindr += 1
                    elif pdisp == None and disp:
                        #print('DIIIIS', int(disp.split()[0])/1000)
                        numz =  "{:.1f}".format(int(disp.split()[0])/1000) 
                        dcarModel_cln[brand][model]['engines'][eng]['Pdisplacement'] = f"{numz}L"
                if len(dcarModel_cln[brand][model]['engines'].keys()) == 0:
                    print("cancello [eng == 0]",brand, model)
                    del dcarModel_cln[brand][model]
                    deletatiByEng += 1
                    continue
                
        print("cancellatiByEng", deletatiByEng)
        print("cancellatiByCilindr", deletatiByCilindr)
                    
    with open(pathFile, 'w') as f:
        json.dump(dcarModel_cln, f)
            
dai()