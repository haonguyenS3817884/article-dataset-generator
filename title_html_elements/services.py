import re
import asyncio
from utils.crawl_handler import fetch_raw_html
from utils.html_handler import default_html_parser
from .models import BaseTitleHTMLElement, CreatingTitleHTMLElement
from .repository import insert_title_html_element

def get_title_html_elements(raw_html: str, title: str):
    soup = default_html_parser(raw_html=raw_html)
    title_html_elements: list[BaseTitleHTMLElement] = []

    for text_node in soup.find_all(string=re.compile(title)):
        direct_tag = text_node.parent
        direct_tag.attrs["tag_name"] = direct_tag.name
        title_html_element = BaseTitleHTMLElement(**direct_tag.attrs)
        title_html_elements.append(title_html_element)
    
    return title_html_elements

def get_title_meta_elements(raw_html: str, title: str):
    soup = default_html_parser(raw_html=raw_html)
    title_html_elements: list[BaseTitleHTMLElement] = []

    for tag in soup.find_all("meta"):
        raw_tag = str(tag)
        pattern = re.compile(title)
        if bool(pattern.search(raw_tag)):
            tag.attrs["tag_name"] = tag.name
            title_html_element = BaseTitleHTMLElement(**tag.attrs)
            title_html_elements.append(title_html_element)
    
    return title_html_elements


async def extract_title_elements(target_url: str, article_title: str):
    try:
        raw_html = await fetch_raw_html(target_url=target_url)
        insert_operations = []
        semaphore = asyncio.Semaphore(50)
        for element in get_title_html_elements(raw_html, article_title):
            insert_operations.append(insert_title_html_element(CreatingTitleHTMLElement(**element.model_dump(exclude_none=True)), semaphore))
        for element in get_title_meta_elements(raw_html, article_title):
            insert_operations.append(insert_title_html_element(CreatingTitleHTMLElement(**element.model_dump(exclude_none=True)), semaphore))
        await asyncio.gather(*insert_operations)
    except Exception as e:
        print(f"Failed to extract raw html: {e}")