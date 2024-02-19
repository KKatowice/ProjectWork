import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

DEBUGZ = True

class ScriptGenerator:
    def __init__(self, url):
        self.url = url
        self.soup = None

    async def scrape_data(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    self.soup = soup
                    return soup


async def scrape_car_brand_data(sp: BeautifulSoup):
    
    # lista quantita auto in produzione
    bi = [y.text for y in sp.find_all('b',{'class':'col-green2'})]
    #trova tutti gli h5 che contengono gli 'a' con href al modello
    sp = sp.find_all('h5')
    all_brands_links = []
    for x in tqdm(range(len(sp)),"scraping car brand data"):
        if bi[x] == '0':
            continue
        #aggiungi tutti i link che hanno modelli in production
        all_brands_links.append(sp[x].find('a',href=True)['href'])

    return all_brands_links


def isPresent(l: list):
    for x in l:
        if "present" in str(x).lower():
            return True
def removeBrandName(s: str, torem: str):
    
    if "-" in torem:
        torem = torem.replace("-"," ")
    #print(f"remove {torem} da {s}")
    return s.replace(torem,"").strip()


async def scrape_car_model_data(lstBrand: list):
    ret = {} #{ brand:{model:{..info}}, ...  }
    for link_brand in tqdm(lstBrand,"scraping car models"):
        nme = link_brand.split("/")[3]
        ret[nme] = {}
        sg = ScriptGenerator(link_brand)
        sg = await sg.scrape_data()
        divCars = sg.find_all('div',{'class':'carmod clearfix'})
        #prendo ogni div che contioene ogni macchina
        for car in divCars:
            isPrnt = isPresent(car.find_all('span'))
            if not isPrnt:
                continue
            #se e' ancora in production aggiungiamo il link alla lista
            mname = removeBrandName(car.h4.text, nme.upper()) #car.h4.text.replace(nme.upper(),"")
            lnk = car.a['href']
            
            ret[nme][mname] = {'link':lnk}

    if DEBUGZ:
        with open('marca_modello.json', 'w') as f:
            json.dump(ret, f)
    return ret
        

def getEngines(divvoneCar: BeautifulSoup, brand: str, model: str):
    boxEngines = divvoneCar.find_all('div',{'class':'mot clearfix'})
    eng = {}
    for x in boxEngines:
        for y in x.find_all('a'):
            #print(y.text)
            #print(y['href'])
            # pulito o no ? TODO
            #nme = y.text.replace(brand.upper(),"").replace(model.upper(),"").rsplit("(")[0].strip()
            eng[y.text] = y['href']
    return eng
    

async def scrape_eachModel_data(dizModels: dict):
    for brand in tqdm(dizModels.keys(),f"scraping models details"):
        for model in dizModels[brand]:
            sg = ScriptGenerator(dizModels[brand][model]['link'])
            sg = await sg.scrape_data()
            divEngines = sg.find_all('div',{'class':'container carmodel clearfix'})
            #print(type(divEngines))
            engList = getEngines(divEngines[0],brand,model)#brand,model dipende se da pulire nome o no @TODO
            dizModels[brand][model]['engines'] = engList
            

    if DEBUGZ:
        with open('marca_modello_engines.json', 'w') as f:
            json.dump(dizModels, f)
    return dizModels
            


async def main(url):
    sg = ScriptGenerator(url)
    sg = await sg.scrape_data()
    lbrand = await scrape_car_brand_data(sg)
    dcarModel = await scrape_car_model_data(lbrand)
    daipls = await scrape_eachModel_data(dcarModel)
     
    
    #print(dcarModel)

async def maintest():
    with open('marca_modello.json', 'r') as f:
        dcarModel = json.load(f)
    daipls = await scrape_eachModel_data(dcarModel)


if __name__ == '__main__':
    url = "https://www.autoevolution.com/cars/"
    #asyncio.run(main(url))
    if DEBUGZ:
        asyncio.run(maintest())
    else:
        asyncio.run(main(url))
        
         