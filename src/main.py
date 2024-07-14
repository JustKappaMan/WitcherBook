import csv
from random import randint
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, ConnectionError, ReadTimeout


def main():
    url = "https://vedmak.fandom.com/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D0%BE%D0%BD%D1%81%D1%82%D1%80%D1%8B_(%D0%92%D0%B5%D0%B4%D1%8C%D0%BC%D0%B0%D0%BA_3)"
    url_parts = urlparse(url)
    url_origin = f"{url_parts.scheme}://{url_parts.hostname}"

    proxies = {"https": f"socks5://127.0.0.1:{randint(9052, 9139)}"}

    database = []
    try:
        response = requests.get(url=url, proxies=proxies)
        soup = BeautifulSoup(response.text, "lxml")
        names_and_links = parse_monsters_names_and_links(soup=soup)
        print("Получили ссылки с главной страницы с монстрами")

        for name, link in names_and_links.items():
            response = requests.get(url=f"{url_origin}{link}", proxies=proxies)
            soup = BeautifulSoup(response.text, "lxml")
            database.append({"Имя": name} | parse_monster_details(soup=soup))
            print(f"Получили информацию о монстре {name}")
    except (ProxyError, ConnectionError, ReadTimeout):
        print("Не удалось подключиться к прокси-серверу, попробуем другой")

    if database:
        with open("WitcherBook.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=database[0].keys(), delimiter=";")
            writer.writeheader()
            writer.writerows(database)


def parse_monsters_names_and_links(soup: BeautifulSoup) -> dict[str, str]:
    """
    Парсинг имён монстров и относительных ссылок на их страницы с главной страницы.
    """
    return {a.get("title"): a.get("href") for a in soup.css.select("div.category-page__member-left a")}


def normalize_multiline_details(node) -> str:
    """
    Приведение солянки из текста, <a> и <br> в строку вида `thing1, thing2, thing3`.
    """
    text = []
    for el in node.children:
        if isinstance(el, str):
            text.append(el)
        elif el.name == "br":
            text.append(", ")
        else:
            text.append(el.get_text())
    return "".join(text)


def parse_monster_details(
    soup: BeautifulSoup,
    details: tuple[str] = ("Класс", "Вид", "Подвиды", "Тип", "Местонахождение", "Тактика", "Иммунитет", "Уязвимость"),
) -> dict[str, str]:
    """
    Парсинг данных о конкретном монстре.
    """
    result = {}
    for detail in details:
        if node := soup.css.select_one(f"div[data-source='{detail}'] .pi-data-value"):
            if node.css.select_one("br"):
                result |= {detail: normalize_multiline_details(node)}
            else:
                result |= {detail: node.get_text()}
        else:
            result |= {detail: "Неизвестно"}
    return result


if __name__ == "__main__":
    main()
