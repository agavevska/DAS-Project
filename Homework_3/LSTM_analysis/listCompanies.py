import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import re


# Функцијата која ја имаш за филтрирање на податоци
def filterOne(browser):
    url = "https://www.mse.mk/mk/stats/symbolhistory/kmb"
    browser.get(url)
    optionsList = browser.find_element(By.ID, "Code")
    filteredOptions = []
    if optionsList is not None:
        options = optionsList.find_elements(By.TAG_NAME, "option")
        for option in options:
            option = option.text.strip()
            if not re.search(r'\d', option):
                filteredOptions.append(option)
    return filteredOptions


# Скрејпирај податоци
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)
filteredOptions = filterOne(browser)

# Испрати ги податоците на Spring серверот преку POST барање
response = requests.post("http://localhost:8080/api/companies", json={"companies": filteredOptions})

# Проверка на одговорот
print(response.status_code)
print(response.json())
