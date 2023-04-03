import json
from pprint import pprint
from random import random, randint
from time import sleep

from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# header = fake_headers.Headers()
#
# print(header)

BASE_URL = 'https://www.avito.ru/moskva'

s = Service(r'C:\Users\админ\pythonProject\avito_project\avito\chromedriver.exe')
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--proxy-server=176.124.46.161:8000')
# options_chrome.add_argument('--proxy-server=waUkt8:RrcmGo@176.124.46.161:8000')
# options_chrome.add_argument('--headless=chrom' )
options_chrome.add_argument('--headless')


# proxy = {
#     'http': 'http://176.124.46.161:8000',
#     'https': 'https://176.124.46.161:8000',
# }

# p = 8.219.105.248:80
# 68.1.210.163:4145
# 176.124.46.161:8000

# params = {
#     'q': 'термос'
# }

def test_ip():
    BASE_URL = 'http://httpbin.org/ip'
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        browser.get(BASE_URL)
        sleep(2)
        id = browser.find_element(By.TAG_NAME, 'pre')
        print(id.text)


def get_avito_info(offer: dict):
    data_list = []
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        # print('начинаю просмотр авито')
        try:
            offer['name'] = offer['name'].replace('оптом', '')
            browser.get(BASE_URL + f'?q={offer["name"]}')
            min_price = int(offer['buy_price'] * 0.5)
            max_price = int(offer['buy_price'] * 5)
            sleep(randint(2, 4))
            browser.implicitly_wait(6)
            count_offer = browser.find_element(By.CSS_SELECTOR, 'span[data-marker="page-title/count"]').text
            ads = browser.find_element(By.CSS_SELECTOR, 'div[data-marker="catalog-serp"]').find_elements(By.CSS_SELECTOR, 'div[data-marker="item"]')
            # print('предложений:', len(offers))
            # print(count_offer)
            for ad in ads:
                # Собираем цены в объявлениях
                try:
                    ad_price = ad.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
                except:
                    ad_price = "Нет цены в объявлении"

                # Собираем url объявлений
                try:
                    ad_url = ad.find_element(By.CSS_SELECTOR, 'div [data-marker="item-title"]').get_attribute("href")
                except:
                    ad_url = "Нет ссылки на объявление"

                # Собираем названия объявлений
                try:
                    ad_name = ad.find_element(By.CSS_SELECTOR, 'h3[itemprop = "name"]').text
                except:
                    ad_name = "Нет названия объявления"

                try:
                    ad_descr_title = ad.find_element(By.XPATH, '//div[@class="iva-item-descriptionStep-C0ty1"]/div').text
                except:
                    ad_descr_title = "Нет описания в объявлении"

                # Собираем время публикации объявлений
                try:
                    ad_publ_time = ad.find_element(By.CSS_SELECTOR, 'div[data-marker="item-date"]').text
                except:
                    ad_publ_time = "Нет времени публикации объявления"

                if ad_price != "Нет цены в объявлении" and min_price < int(ad_price) < max_price:
                    data_list.append({
                        'name': ad_name,
                        'price': int(ad_price),
                        'disc': ad_descr_title,
                        'pablic_at': ad_publ_time,
                        'url': ad_url,
                        })
            print()
            print('позиция', offer['name'])
            print('предложений',len(data_list))
            count = sum([1 for x in data_list if x != 'Нет цены в объявлении'])
            avg = sum([x['price'] for x in data_list])
            avg_sell = int(avg/count)
            print('средняя цена',avg_sell)
            print('интересная цена',offer['buy_price'] * 1.7)

            offer['avg_price'] = avg_sell
            offer['count_offer'] = int(count_offer)
            offer['url_avito'] = browser.current_url
            return offer

        except:
            return 'Нет данных/ Ошибка'



def get_avito_info_0(offers: list[dict, dict]):
    '''

    Старая версия, пока оставил
    '''
    answer_list = []
    data_list = []
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        print('начинаю просмотр авито')
        for offer in tqdm(offers):
            try:
                browser.get(BASE_URL + f'?q={offer["name"]}')
                min_price = int(offer['buy_price'] * 0.5)
                max_price = int(offer['buy_price'] * 5)
                sleep(randint(2, 4))
                browser.implicitly_wait(6)
                count_offer = browser.find_element(By.CSS_SELECTOR, 'span[data-marker="page-title/count"]').text
                ads = browser.find_element(By.CSS_SELECTOR, 'div[data-marker="catalog-serp"]').find_elements(By.CSS_SELECTOR, 'div[data-marker="item"]')
                # print('предложений:', len(offers))
                # print(count_offer)
                for ad in ads:
                    # Собираем цены в объявлениях
                    try:
                        ad_price = ad.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
                    except:
                        ad_price = "Нет цены в объявлении"

                    # Собираем url объявлений
                    try:
                        ad_url = ad.find_element(By.CSS_SELECTOR, 'div [data-marker="item-title"]').get_attribute("href")
                    except:
                        ad_url = "Нет ссылки на объявление"

                    # Собираем названия объявлений
                    try:
                        ad_name = ad.find_element(By.CSS_SELECTOR, 'h3[itemprop = "name"]').text
                    except:
                        ad_name = "Нет названия объявления"

                    try:
                        ad_descr_title = ad.find_element(By.XPATH, '//div[@class="iva-item-descriptionStep-C0ty1"]/div').text
                    except:
                        ad_descr_title = "Нет описания в объявлении"

                    # Собираем время публикации объявлений
                    try:
                        ad_publ_time = ad.find_element(By.CSS_SELECTOR, 'div[data-marker="item-date"]').text
                    except:
                        ad_publ_time = "Нет времени публикации объявления"

                    if ad_price != "Нет цены в объявлении" and min_price < int(ad_price) < max_price:
                        data_list.append({
                            'name': ad_name,
                            'price': int(ad_price),
                            'disc': ad_descr_title,
                            'pablic_at': ad_publ_time,
                            'url': ad_url,
                            })
                print()
                print('позиция', offer['name'])
                print('предложений',len(data_list))
                count = sum([1 for x in data_list if x != 'Нет цены в объявлении'])
                avg = sum([x['price'] for x in data_list])
                avg_sell = int(avg/count)
                print('средняя цена',avg_sell)
                print('интересная цена',offer['buy_price'] * 1.7)
                if avg_sell > offer['buy_price'] * 1.7:
                    offer['avg_price'] = avg_sell
                    offer['count_offer'] = int(count_offer)
                    offer['url_avito'] = browser.current_url
                    answer_list.append(offer)
                sleep(randint(1,5))
            except:
                continue
    return answer_list

def write_json(data):
    with open( 'files/offers.json', 'w', encoding='utf-8') as file:
        # for num, offer in enumerate(data, 1):
        #     offer['id'] = num
            json.dump(data, file, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=False)

def get_parse_avito(offers):
    write_json(get_avito_info(offers))

if __name__ == '__main__':
    # test_ip()
    # offers = [{'name': 'Увлажнитель воздуха с кошечкой', 'url': 'https://trend-opt.ru/katalog/tovary-dlya-doma/uvlazhnitel-vozduha/uvlazhnitel-vozduha-s-koshechkoj/', 'buy_price': 540, 'min_buy': '2'},
    #           {'name': 'Ручная лапшерезка', 'url': 'https://trend-opt.ru/katalog/tovary-dlya-doma/tovary-dlya-kuhni/ruchnaya-lapsherezka/', 'buy_price': 780, 'min_buy': '1'},
    #           {'name':'Набор кухонных принадлежностей с держателем', 'buy_price': 920, 'min_buy': 1, 'link': 'https://trend-opt.ru/katalog/tovary-dlya-doma/plitka-dlya-rozzhiga-uglej/'},
    #           ]
    # a = get_avito_info(offers)
    # print(a)

    test_avito = [{'name': 'Ручная лапшерезка', 'url': 'https://trend-opt.ru/katalog/tovary-dlya-doma/tovary-dlya-kuhni/ruchnaya-lapsherezka/', 'buy_price': 780, 'min_buy': '1', 'avg_price': 1539, 'count_offer': '148', 'url_avito': 'https://www.avito.ru/moskva?q=%D0%A0%D1%83%D1%87%D0%BD%D0%B0%D1%8F+%D0%BB%D0%B0%D0%BF%D1%88%D0%B5%D1%80%D0%B5%D0%B7%D0%BA%D0%B0'},
                  {'name':'Набор кухонных принадлежностей с держателем', 'buy_price': 920, 'min_buy': 1, 'link': 'https://trend-opt.ru/katalog/tovary-dlya-doma/plitka-dlya-rozzhiga-uglej/'}]
    write_json(test_avito)