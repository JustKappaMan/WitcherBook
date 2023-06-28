import requests
from bs4 import BeautifulSoup
import random
import csv
from config import headers  # my "user agent" and "accept"

URL = "https://vedmak.fandom.com/wiki/Ignis_Fatuus"


proxy_tor = "socks5://127.0.0.1:" + str(random.randint(9052, 9139))
proxies = {"https": proxy_tor}

FILENAME = 'WitcherBook'


with open("index.html", "r") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
beast_class = soup.find("div", {'data-source': "Класс"}).find("a").get("title")
beast_variation = soup.find("div", {'data-source': "Вид"}).find("a").get("title")
beast_type = soup.find("div", {'data-source': "Тип"}).find("div").text
print(beast_type)

