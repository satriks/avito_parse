from sqlalchemy import create_engine, text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

s = Service(r'C:\Users\админ\pythonProject\avito_project\avito\chromedriver.exe')
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--headless')


def get_my_ip():
    BASE_URL = 'http://httpbin.org/ip'
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        browser.get(BASE_URL)
        id = browser.find_element(By.TAG_NAME, 'pre')
        print(id.text)

def from_sql_to_exel():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/product')

    data = pd.read_sql_query(sql=text('''SELECT * 
                                FROM products p 
                                JOIN avito a ON p.id = a.product_id
                                WHERE a.avito_id IS NOT NULL AND a.avg_price > p.buy_price 
                                ORDER BY a.count_offer DESC ;'''), con=engine.connect())
    data.to_excel("files/output.xlsx")

if __name__ == '__main__':
    from_sql_to_exel()