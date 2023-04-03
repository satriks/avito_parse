from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm

from db.ORM import add_product

s = Service(r'C:\Users\админ\pythonProject\avito_project\avito\chromedriver.exe')
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--proxy-server=176.124.46.161:8000')
# options_chrome.add_argument('--proxy-server=waUkt8:RrcmGo@176.124.46.161:8000')
# options_chrome.add_argument('--headless=chrom' )
options_chrome.add_argument('--headless')

def get_all_categori():
    categori_list = []
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        browser.get('https://trend-opt.ru/')
        cat = browser.find_element(By.CLASS_NAME, 'aside_categories').find_elements(By.TAG_NAME, 'a')
        for el in cat:
            categori_list.append(el.get_attribute('href'))
    return categori_list

def get_offer_page(link_list):
    offers_list = []
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        print('Собираю предложения поставщика trend_opt, со страницы новинки')
        for link in tqdm(link_list, colour='#7fffd4', desc='Категории'):
            try:
                browser.get(link)
                a = browser.find_elements(By.CLASS_NAME, "product-layout")
                sleep(1)
                print('Обрабатываю предложения')
                for i in tqdm(a, colour='yellow', unit='Предложений'):
                    price = int(i.find_element(By.CLASS_NAME, 'new_price').text.split()[0])
                    if price > 400:
                        offers_list.append({
                            'name': i.find_element(By.TAG_NAME, 'h3').text,
                            'url': i.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                        })
            except:
                continue
    return offers_list

def get_price_offer(offers_list):
    offers = []
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        print('Начинаю сбор цен')
        for url in tqdm(offers_list, colour='green', unit='Получаю цены'):
            browser.get(url['url'])
            tbody = browser.find_element(By.TAG_NAME, 'tbody')
            data_tboby = tbody.find_element(By.CLASS_NAME, 'price_tr').find_elements(By.TAG_NAME, 'td')
            try:
                buy_price = int(data_tboby[1].text.replace('Р', '').replace(' ', ''))
            except:
                buy_price = 'нет цены'
            try:
                min_buy = data_tboby[0].text.split()[0]
            except:
                min_buy = 'Не указан минимум'
            url['buy_price'] = buy_price
            url['min_buy'] = int(min_buy)
            offers.append(url)
    return offers

def get_trend_opt():
    for data in tqdm(get_price_offer(get_offer_page(get_all_categori())), colour='blue', unit='продуктов', desc='Запись в БД' ):
        add_product(data)


if __name__ == '__main__':
    get_trend_opt()
    # data = (get_all_categori())
    # print(len(data))
    # print(*data, sep='\n')