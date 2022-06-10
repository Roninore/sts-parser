from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime

print('Введи дату в формате yyyy-mm-dd')
date = input()

url = 'https://tv.yandex.ru/channel/sts-8?date=' + date
page = requests.get(url)

# jsonP = page.json().window
# print(jsonP)

soup = BeautifulSoup(page.text, 'html5lib')

scr = soup.find_all('script')[9]


text = BeautifulSoup(scr.prettify(), 'html.parser')

# print(text)

def convertToDate(str):
    return datetime.strptime(str.split('+')[0],r'%Y-%m-%dT%H:%M:%S') 

def getTimeStr(date):
    return date.strftime("%H:%M")


m = re.search(r"window.__INITIAL_STATE__ = (.*?);", scr.string)
if m:
    data = json.loads(m.group(1))
    for program in data["channel"]["schedule"]["events"]:
        start = convertToDate(program["start"])
        finish = convertToDate(program["finish"])
        if (finish > datetime.now()):
            if (start < datetime.now()):
                print("Сейчас в эфире ==>",end=" ")
            print(program["program"]["title"], end=" ")
            print(getTimeStr(start) + " - " + getTimeStr(finish))
