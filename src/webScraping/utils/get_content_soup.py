from bs4 import BeautifulSoup

def get_content_soup(dic):
    html = dic["content"]
    soup = BeautifulSoup(html, "html.parser")
    return soup