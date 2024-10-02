import requests


def get_content(url):
    response = requests.get(url)
    content = response.text
    return content
