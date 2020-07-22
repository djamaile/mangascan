import requests
from bs4 import BeautifulSoup
from core.exceptions import RetrievingMangaException
from typing import List
from dataclasses import asdict
from helper.manga import Manga


def get_viz() -> List[Manga]:
    date = "21-7-2020".split("-")
    year = date[2]
    month = "0" + date[1] if int(date[1]) < 10 else date[1]
    URL = f"https://www.viz.com/calendar/{year}/{month}"
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")
        manga = []
        table = soup.select("article[class^=g-3]")

        for row in table:
            img = row.figure.a.img["data-original"]
            rowUnder = row.select("div[class^=pad-x-md]")
            name = None
            link = None
            for n in rowUnder:
                name = n.h4.a.text
                link = f"viz.com{n.h4.a['href']}"
            manga.append(asdict(Manga(name=name, img=img, link=link, publisher="viz")))
        return manga
    except requests.RequestException as e:
        raise RetrievingMangaException(
            "Something went wrong retrieving viz manga",
            status_code=e.response.status_code,
        )


def get_yen() -> List[Manga]:
    URL = "https://yenpress.com/new-releases/"
    manga = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")
        table = soup.findAll("li", attrs={"class": "book-shelf-title-grid"})
        for row in table:
            name = row.img["data-title"]
            img = row.img["src"].rsplit("?", 1)[0]
            detail = row.findAll("div", attrs={"class": "book-detail-links"})
            link = "https://yenpress.com" + detail[0].a["href"]
            manga.append(
                asdict(Manga(name=name, img=img, link=link, publisher="yen press"))
            )
        return manga
    except requests.RequestException as e:
        raise RetrievingMangaException(
            "Something went wrong retrieving yenpress manga",
            status_code=e.response.status_code,
        )


def get_seven_seas() -> List[Manga]:
    URL = "https://sevenseasentertainment.com/release-dates/"
    manga = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")
        table = soup.findAll(
            "div",
            attrs={
                "style": "float: left; margin: 0 3px 10px 6px; width: 134px; height: 189px; background: #CECECE;"
            },
        )
        for row in table:
            name = row.a["title"]
            img = row.img["srcset"]
            link = row.a["href"]
            for remove in ["135w", "320w"]:
                if remove in img:
                    img = img.replace(remove, "")
            img = img.split(",")
            img = img[len(img) - 1]
            manga.append(
                asdict(Manga(name=name, img=img, link=link, publisher="seven seas"))
            )
        return manga
    except requests.RequestException as e:
        raise RetrievingMangaException(
            "Something went wrong retrieving sevenseas manga",
            status_code=e.response.status_code,
        )


def get_dark_horse() -> List[Manga]:
    date = "21-7-2020"
    months = {
        "1": "Jan",
        "2": "Feb",
        "3": "Mar",
        "4": "May",
        "5": "Apr",
        "6": "Jun",
        "7": "Jul",
        "8": "Aug",
        "9": "Sep",
        "10": "Okt",
        "11": "Nov",
        "12": "Dec",
    }

    month = months[date.split("-")[1]]
    year = date.split("-")[2]
    manga = []

    try:
        URL = f"https://www.darkhorse.com/Books/Browse/Manga---{month}+{year}-{month}+{year}/P9wdwkt8"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")

        table = soup.findAll("div", attrs={"class": "list_item"})
        for row in table:
            img = row.find("a", attrs={"class": "product_link"}).img["src"]
            link = f"darkhorse.com{row.a['href']}"
            name = row.findAll("a", attrs={"class": "product_link"})[
                2
            ].text  # access link that has the manga name
            manga.append(
                asdict(Manga(name=name, img=img, link=link, publisher="darkhorse"))
            )
        return manga
    except requests.RequestException as e:
        raise RetrievingMangaException(
            "Something went wrong retrieving darkhorse manga",
            status_code=e.response.status_code,
        )


def get_kodansha():
    print("hallo")
    URL = "https://kodanshacomics.com/new-releases/"
    manga = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")
        table = soup.findAll("article", "card card--no-outline release-card")

        for row in table:
            name = row.h4.cite.text
            link = row.h4.a["href"]
            manga.append(
                asdict(Manga(name=name, img="placeholder", link=link, publisher="kodansha"))
            )
        return manga
    except requests.RequestException as e:

        raise RetrievingMangaException(
            "Something went wrong retrieving kondansha manga",
            status_code=e.response.status_code,
        )


def get_manga_image_of_kodansha(url: str):
    r = requests.get(url)
    s = requests.session()
    soup = BeautifulSoup(r.content, "html5lib")
    row = soup.find("div", attrs={"class": "sidebar"})
    s.cookies.clear()
    if row:
        return row.img["src"]
    else:
        return "placeholder"

