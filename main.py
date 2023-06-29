import requests
from bs4 import BeautifulSoup
import random
import csv
from config import headers  # my "user agent" and "accept"

URL = "https://vedmak.fandom.com/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D0%BE%D0%BD%D1%81%D1%82%D1%80%D1%8B_(%D0%92%D0%B5%D0%B4%D1%8C%D0%BC%D0%B0%D0%BA_3)"

proxy_tor = "socks5://127.0.0.1:" + str(random.randint(9052, 9139))
proxies = {"https": proxy_tor}

FILENAME = 'WitcherBook'

# TODO:
"""
1) don't write empty rows to file +
2) asyncio?
"""


def parse_monster_characteristic(soup_obj, parameter):
    try:
        res = ''
        monster_characteristic = soup_obj.find("aside",
                                               class_="portable-infobox pi-background "
                                                      "pi-border-color pi-theme-Ведьмак-3 pi-layout-default")
        if monster_characteristic is None:
            monster_characteristic = soup_obj.find("aside",
                                                   class_="portable-infobox pi-background "
                                                          "pi-border-color pi-theme-Каменные-сердца pi-layout-default")
        if monster_characteristic is None:
            monster_characteristic = soup_obj.find("aside",
                                                   class_="portable-infobox pi-background "
                                                          "pi-border-color pi-theme-Кровь-и-Вино pi-layout-default")
        if monster_characteristic is None:
            return
        if parameter == 'Имя':
            monster_characteristic = monster_characteristic.find("h2").text
            res = monster_characteristic
            return res
        else:
            monster_characteristic = monster_characteristic.find("div", {'data-source': parameter}).find("div")
            for el in monster_characteristic:
                res += " " + el.text
            return res.strip()
    except AttributeError:
        return "Неизвестно"


def get_monster_name_and_link(soup_obj):
    links = {}
    allmonsters = soup_obj.find_all("div", class_="category-page__members-wrapper")
    for i in range(1, len(allmonsters)):
        monsters_curr_letter = allmonsters[i].find("ul")
        for monsters in monsters_curr_letter:
            monster = monsters.find("a")
            if str(monster) == '-1':
                pass
            elif monster.get("title") == "Монстры (Ведьмак 3)":
                pass
            else:
                links[monster.get("title")] = (monster.get("href"))
    return links


def file_write_headers(filename):
    with open(f"{filename}.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ("Имя", "Класс", "Вид", "Подвиды", "Тип", "Местонахождение", "Тактика", "Иммунитет", "Уязвимость"))


def file_write_data(filename, soup_obj):
    with open(f"{filename}.csv", "a", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        if parse_monster_characteristic(soup_obj, "Имя"):
            writer.writerow(
                (parse_monster_characteristic(soup_obj, "Имя"),
                 parse_monster_characteristic(soup_obj, "Класс"),
                 parse_monster_characteristic(soup_obj, "Вид"),
                 parse_monster_characteristic(soup_obj, "Подвиды"),
                 parse_monster_characteristic(soup_obj, "Тип"),
                 parse_monster_characteristic(soup_obj, "Местонахождение"),
                 parse_monster_characteristic(soup_obj, "Тактика"),
                 parse_monster_characteristic(soup_obj, "Иммунитет"),
                 parse_monster_characteristic(soup_obj, "Уязвимость")
                 )
        )


def main():
    url_first_part = '/'.join(URL.split('/')[:3])  # https://vedmak.fandom.com
    file_write_headers(filename=FILENAME)
    try:
        response = requests.get(url=URL, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.text, "lxml")
        links = get_monster_name_and_link(soup_obj=soup)
        print("Перешли на главную страницу\nПолучили ссылки на страницы с монстрами")
        for monster_name, monster_link in links.items():
            monster_page = requests.get(url=url_first_part + monster_link, headers=headers, proxies=proxies)
            monster = BeautifulSoup(monster_page.text, "lxml")
            file_write_data(filename=FILENAME, soup_obj=monster)
            print(f"Спарсили информацию о монстре {monster_name}")
    except requests.exceptions.ProxyError:
        print("\nНе удалось подключиться к прокси-серверу, попробуем другой\n")
    except requests.exceptions.ConnectionError:
        print("\nНе удалось подключиться к прокси-серверу, попробуем другой\n")
    except requests.exceptions.ReadTimeout:
        print("\nПревышен таймаут подключения к серверу, попробуем другой\n")
    except AttributeError:
        print("\nАйпишник в бане :с\n")


if __name__ == '__main__':
    main()
