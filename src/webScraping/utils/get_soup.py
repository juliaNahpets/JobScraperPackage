from webScraping.utils.get_content import get_content
from bs4 import BeautifulSoup


def get_soup(url):
    content = get_content(url)
    soup = BeautifulSoup(content, "html.parser")
    return soup


def get_content_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_file_soup(file_path):
    with open(file_path, mode="r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")
    return soup
