from bs4 import BeautifulSoup

def default_html_parser(raw_html: str):
    return BeautifulSoup(raw_html, "html.parser")