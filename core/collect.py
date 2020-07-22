import requests
import cfscrape
from bs4 import BeautifulSoup
from core.exceptions import RetrievingMangaException
from typing import List
from dataclasses import asdict
from helper.manga import Manga
from utils.logger import init_logger
from datetime import datetime, timezone

logger = init_logger(__name__)


def get_html(url: str, publisher: str) -> BeautifulSoup:
    logger.debug(f"Trying to retrieve new releases from publisher {publisher}")
    r = requests.get(url)
    return BeautifulSoup(r.content, "html5lib")


def get_viz() -> List[Manga]:
    """
    Viz url needs a date, if the month is < 12, then add leading zero
    """
    date = (
        datetime.now(timezone.utc).strftime("%d-%m-%y").split("-")
    )  # split date into d m y
    year = "20" + date[2]
    month = date[1]
    URL = f"https://www.viz.com/calendar/{year}/{month}"

    try:
        soup = get_html(URL, "viz")
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
        logger.error(e)
        raise RetrievingMangaException(
            "Something went wrong retrieving viz manga",
            status_code=e.response.status_code,
        )


def get_yen() -> List[Manga]:
    URL = "https://yenpress.com/new-releases/"
    manga = []

    try:
        soup = get_html(URL, "yen press")
        table = soup.findAll("li", attrs={"class": "book-shelf-title-grid"})
        for row in table:
            name = row.img["data-title"]
            img = row.img["src"].rsplit("?", 1)[0]  # remove ?/.. string from img
            detail = row.findAll("div", attrs={"class": "book-detail-links"})
            link = "https://yenpress.com" + detail[0].a["href"]  # detail link of manga
            manga.append(
                asdict(Manga(name=name, img=img, link=link, publisher="yen press"))
            )
        return manga
    except requests.RequestException as e:
        logger.error(e)
        raise RetrievingMangaException(
            "Something went wrong retrieving yenpress manga",
            status_code=e.response.status_code,
        )


def get_seven_seas() -> List[Manga]:
    URL = "https://sevenseasentertainment.com/release-dates/"
    manga = []

    try:
        soup = get_html(URL, "seven seas")
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
            for remove in ["135w", "320w"]:  # images have 135w & 320w in their name
                if remove in img:
                    img = img.replace(remove, "")
            img = img.split(",")
            img = img[len(img) - 1]  # get the first img of the set of images
            manga.append(
                asdict(Manga(name=name, img=img, link=link, publisher="seven seas"))
            )
        return manga
    except requests.RequestException as e:
        logger.error(e)
        raise RetrievingMangaException(
            "Something went wrong retrieving sevenseas manga",
            status_code=e.response.status_code,
        )


def get_dark_horse() -> List[Manga]:
    """ Darkhorse link needs a date and year  """
    date = datetime.now(timezone.utc).strftime("%d-%m-%y")
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

    month = months[date.split("-")[1].lstrip("0")]  # remove leading zero
    year = date.split("-")[2]
    URL = f"https://www.darkhorse.com/Books/Browse/Manga---{month}+{year}-{month}+{year}/P9wdwkt8"
    manga = []

    try:
        soup = get_html(URL, "darkhorse")
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
        logger.error(e)
        raise RetrievingMangaException(
            "Something went wrong retrieving darkhorse manga",
            status_code=e.response.status_code,
        )


def get_kodansha() -> List[Manga]:
    """
    One problem with scraping Kodansha is that they only display their manga titles
    They don't show the images of the manga
    To get the image we have scrape the detail page of the manga
    which increases the requests from 1 to 1..k, k = amount of titles on page
    :return:
    """
    URL = "https://kodanshacomics.com/new-releases/"
    manga = []

    try:
        soup = get_html(URL, "kodansha")
        table = soup.findAll("article", "card card--no-outline release-card")
        for row in table:
            name = row.h4.cite.text
            link = row.h4.a["href"]
            manga.append(
                asdict(
                    Manga(name=name, img="placeholder", link=link, publisher="kodansha")
                )
            )
        return manga
    except requests.RequestException as e:
        logger.error(e)
        raise RetrievingMangaException(
            "Something went wrong retrieving kondansha manga",
            status_code=e.response.status_code,
        )


def get_manga_image_of_kodansha(url: str, name: str):
    """
    Kodansha website uses cloudflare to block requests, if there are to many coming in
    Currently using package cfscrape to bypass their protection
    It can happen that a requested page is returned without a image
    In that case return 'placeholder', so that the front-end can put in a default picture

    Or we can put the manga name in a queue and continue till there are no more objects in the queue
    This is a function is in development and needs to be improved. So, for now it's best not used.
    """
    scraper = cfscrape.create_scraper()
    soup = BeautifulSoup(scraper.get(url).content, "html5lib")
    row = soup.find("div", attrs={"class": "sidebar"})
    try:
        return row.img["src"]
    except (TypeError, AttributeError):
        logger.debug(f"Could not get the image of {name}, link is: {url}")
        return "placeholder"
