import json
import asyncio
#import aiohttp
#from bs4 import BeautifulSoup
#from scraper import ScrapeGenerator
#import time
import re
from tqdm import tqdm
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def convert_to_integer(number_str):
    pattern = r',\d{2}$' 
    pattern2 = r'.\d{2}$'  
    if re.search(pattern, number_str):
        number_str = re.sub(pattern, '', number_str)
    elif re.search(pattern2, number_str):
        number_str = re.sub(pattern2, '', number_str)
    return int(number_str.replace(',', '').replace('.', ''))


def seleniumscrape(link):
    
    chrome_driver_path = "/usr/bin/chromium-browser"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    chrome_options.binary_location = chrome_driver_path
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(link)
    acc = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='L2AGLb']")))
    acc.click()
    element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='dURPMd']")))
    #print(element.text)
    reg = r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})' #TODO add check for things like "$2.5 million"
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
                #nme = x+" "+y+" price"
                lnk = f'https://www.google.com/search?q={x}+{y}+price'
                #print(lnk)
                pricez = seleniumscrape(lnk)
                dcarModel[x][y]['price'] = pricez


        with open('completo_wPrices.json', 'w') as f:
            json.dump(dcarModel, f)
            

asyncio.run(scrapePrices())