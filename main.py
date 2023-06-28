import requests
from bs4 import BeautifulSoup
import random
import csv
from config import headers  # my "user agent" and "accept"

URL = "https://vedmak.fandom.com/wiki/%D0%A1%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%B8%D1%81%D1%82%D1%8B%D0%B9_%D0%B2%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D1%81%D0%BA"

proxy_tor = "socks5://127.0.0.1:" + str(random.randint(9052, 9139))
proxies = {"https": proxy_tor}

FILENAME = 'WitcherBook'

with open("index.html", "r") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")


def parse_beast_class(soup_obj):
    try:
        beast_class = soup_obj.find("aside",
                                    class_="portable-infobox pi-background "
                                           "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        beast_class = beast_class.find("div", {'data-source': "Класс"}).find("a").get("title")
        return beast_class
    except AttributeError:
        return "Нет данных о классе"


def parse_beast_variation(soup_obj):
    try:
        beast_variation = soup_obj.find("aside",
                                        class_="portable-infobox pi-background "
                                               "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        beast_variation = beast_variation.find("div", {'data-source': "Вид"}).find("a").get("title")
        return beast_variation
    except AttributeError:
        return "Нет данных о виде"


def parse_beast_type(soup_obj):
    try:
        beast_type = soup_obj.find("aside",
                                   class_="portable-infobox pi-background "
                                          "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        beast_type = beast_type.find("div", {'data-source': "Тип"}).find("div").text
        return beast_type
    except AttributeError:
        return "Нет данных о типе"


def parse_beast_location(soup_obj):
    beast_location = soup_obj.find("aside",
                                   class_="portable-infobox pi-background "
                                          "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
    if beast_location is None:
        beast_location = soup_obj.find("aside",
                                       class_="portable-infobox pi-background "
                                              "pi-border-color pi-theme-Кровь-и-Вино pi-layout-default")
    if beast_location is None:
        beast_location = soup_obj.find("aside",
                                       class_="portable-infobox pi-background "
                                              "pi-border-color pi-theme-Каменные-сердца pi-layout-default")
    try:
        beast_location = beast_location.find("div", {'data-source': "Местонахождение"}).find("div").text
        return beast_location
    except AttributeError:
        return "Нет данных об обитании"


def parse_beast_tactic(soup_obj):
    try:
        beast_tactic = soup_obj.find("aside",
                                     class_="portable-infobox pi-background "
                                            "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        beast_tactic = beast_tactic.find("div", {'data-source': "Тактика"}).find("div").text
        return beast_tactic
    except AttributeError:
        return "Нет данных о тактике"
# there may be no tactic (exception AttributeError)


def parse_beast_weakness(soup_obj):
    try:
        res = ''
        beast_weakness = soup_obj.find("aside",
                                       class_="portable-infobox pi-background "
                                              "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        beast_weakness = beast_weakness.find("div", {'data-source': "Уязвимость"}).find("div").find_all("a")
        for i in range(len(beast_weakness)):
            res += beast_weakness[i].text
            if i != len(beast_weakness) - 1:
                res += ', '
        return res
    except AttributeError:
        return "Нет данных об уязвимостях"


print(parse_beast_location(soup))
