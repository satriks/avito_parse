from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

s = Service(r'C:\Users\админ\pythonProject\avito_project\avito\chromedriver.exe')
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--headless')


def get_my_ip():
    BASE_URL = 'http://httpbin.org/ip'
    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        browser.get(BASE_URL)
        id = browser.find_element(By.TAG_NAME, 'pre')
        print(id.text)