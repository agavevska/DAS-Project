from gettext import install

import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime, timedelta
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)

def replaceDots(price_string):
    price_string = price_string.replace(".", "'")
    price_string = price_string.replace(",", ".")
    price_string = price_string.replace("'", ",")
    return price_string

def readFile(list_dict):
   df = pd.read_csv('companies.csv')
   data = df.to_dict(orient='records')
   if len(list_dict) > 0:
       for l in list_dict:
           data.append(l)
   df=pd.DataFrame(data)
   df.to_csv("companies.csv", index=False)


def getAtt(start_date, end_date, firm_code):
    url = "https://www.mse.mk/mk/stats/symbolhistory/kmb"
    list_dict = []
    session = requests.Session()
    payload = {
        "FromDate": start_date,
        "ToDate": end_date,
        "Code": firm_code
    }
    response = session.post(url, data=payload)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            for tr in table.find_all('tr')[1:]:
                cells = tr.find_all('td')
                if cells[7].text.strip() != '0':
                    information = {
                        "Име": firm_code,
                        "Датум": cells[0].text.strip(),
                        "Цена на последна трансакција": replaceDots(cells[1].text.strip()),
                        "Мак.": replaceDots(cells[2].text.strip()),
                        "Мин.": replaceDots(cells[3].text.strip()),
                        "Просечна цена": replaceDots(cells[4].text.strip()),
                        "%пром.": cells[5].text.strip(),
                        "Количина": replaceDots(cells[6].text.strip()),
                        "Промет во БЕСТ во денари": replaceDots(cells[7].text.strip()),
                        "Вкупен промет во денари": replaceDots(cells[8].text.strip())
                    }
                    list_dict.append(information)
    return list_dict



def filterOne():
 url="https://www.mse.mk/mk/stats/symbolhistory/kmb"
 browser.get(url)
 optionsList=browser.find_element(By.ID, "Code")
 filteredOptions=[]
 if optionsList is not None:
    options=optionsList.find_elements(By.TAG_NAME, "option")
    for option in options:
        option=option.text.strip()
        if bool(re.search(r'\d', option)) is not True:
            filteredOptions.append(option)
 return filteredOptions

def filterTwo(name):
  array_dates=[]
  postoi=False
  if os.path.exists("companies.csv") is False:
      return name + ":The file doesn't exist"
  else:
      data = pd.read_csv('companies.csv')
      for index, row in data.iterrows():
          if row["Име"]==name:
            postoi=True
            array_dates.append(row['Датум'])
      if postoi is False:
          return name + ":There is no informations about this code"
      else:
          date_objects = [datetime.strptime(date, '%d.%m.%Y') for date in array_dates]
          newest_date = max(date_objects)
          newest_date_str = newest_date.strftime('%d.%m.%Y')
          return name + ":" + newest_date_str

def filterThree(input):
  parts=input.split(":")
  code=parts[0]
  string=parts[1]
  list_dict = []
  if string=="The file doesn't exist" or string=="There is no informations about this code":
      end=datetime.now()
      start = end - timedelta(days=365)
      start = start.strftime("%d.%m.%Y")
      end=end.strftime("%d.%m.%Y")
      for i in range(1, 11):
        list_dict.extend(getAtt(start, end, code))
        temp=datetime.strptime(start, "%d.%m.%Y")
        new_date = temp - timedelta(days=365)
        start = new_date.strftime("%d.%m.%Y")
        temp1=datetime.strptime(end, "%d.%m.%Y")
        new_date = temp1 - timedelta(days=365)
        end = new_date.strftime("%d.%m.%Y")
  if string=="The file doesn't exist":
     df=pd.DataFrame(list_dict)
     df.to_csv("companies.csv", index=False)
  elif string=="There is no informations about this code":
          readFile(list_dict)
  else:
     end=datetime.now()
     lastDate=datetime.strptime(string, "%d.%m.%Y")
     lastDate = lastDate + timedelta(days=1)
     date_diff = end - lastDate
     if date_diff.days < 365:
        end=end.strftime("%d.%m.%Y")
        lastDate=lastDate.strftime("%d.%m.%Y")
        list_dict=getAtt(lastDate, end, code)
        readFile(list_dict)
     else:
        ran=date_diff.days // 365

        for i in range(0, ran):

            start = end - timedelta(days=365)
            start = start.strftime("%d.%m.%Y")
            end = end.strftime("%d.%m.%Y")
            list_dict.extend(getAtt(start, end, code))
            temp1=datetime.strptime(end, "%d.%m.%Y")
            new_date = temp1 - timedelta(days=365)
            end = new_date.strftime("%d.%m.%Y")
            end=datetime.strptime(end, "%d.%m.%Y")
        lastDate=lastDate.strftime("%d.%m.%Y")
        list_dict.extend(getAtt(lastDate, start, code))
        readFile(list_dict)


def pipe():
    codes = filterOne()
    results=[]
    for code in codes:
        filterThree(filterTwo(code))
        print(code)


start = time.time()

pipe()

end = time.time()
duration= end - start
print(f"Program finished in {duration:.2f}")

