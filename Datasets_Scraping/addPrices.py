import json
import asyncio
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def convert_to_integer(number_str):
    print("-----",number_str)
    pattern = r'\.\d{2}$' 
    pattern2 = r',\d{2}$'  
    if re.search(pattern, number_str):
        print(number_str)
        number_str = number_str.split(".")[0] #re.sub(pattern, '', number_str)
        print(number_str)
    elif re.search(pattern2, number_str):
        print(number_str)
        number_str = number_str.split(",")[0] #re.sub(pattern2, '', number_str)
        print(number_str)
    return int(number_str.replace(',', '').replace('.', ''))


def seleniumscrape(link):
    
    chrome_driver_path = "/usr/bin/chromium-browser"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = chrome_driver_path
    browser = webdriver.Chrome(options=chrome_options)
    #sposta fori dalla funz /\
    browser.get(link)
    acc = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='L2AGLb']")))
    acc.click()
    element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='dURPMd']")))
    #print(element.text)
    reg = r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?' #TODO check if regex works, added ?
    fnda = re.findall(reg, element.text) 
    numbers = []
    try:
        for num in fnda:
            numbers.append(convert_to_integer(num))
        max_number = max(numbers)
        #print("aaaaaaaaaaaaAAA",numbers, max_number)
        #print("------------------")
    except Exception as e:
        max_number = 0
        print(f"error \n{e}\nON {link}")
    #print(max_number)
    browser.quit()
    return max_number



async def scrapePrices():
    with open('completo.json', 'r') as f:
        dcarModel = json.load(f)
        for x in tqdm(dcarModel, f"scraping prices"):
            #print(x)
            for y in dcarModel[x]:
                if y == "imglink": continue
                #nme = x+" "+y+" price" #TODO SPLIITTARE IL NOME PER RENDERLO PIU DECENTE 
                lnk = f'https://www.google.com/search?q={x}+{y}+price'
                #print(lnk)
                pricez = seleniumscrape(lnk)
                dcarModel[x][y]['price'] = pricez


        with open('completo_wPrices.json', 'w') as f:
            json.dump(dcarModel, f)
            

asyncio.run(scrapePrices())