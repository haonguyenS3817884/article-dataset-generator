import re
import asyncio
from utils.crawl_handler import fetch_raw_html
from utils.html_handler import default_html_parser
from .models import BaseHTMLElement, CreatingHTMLElement, HTMLElementType
from .repository import insert_html_element

def get_html_elements_having_content(raw_html: str, content: str, html_element_type: HTMLElementType):
    soup = default_html_parser(raw_html=raw_html)
    html_elements: list[BaseHTMLElement] = []

    for text_node in soup.find_all(string=re.compile(content)):
        direct_tag = text_node.parent
        html_element = BaseHTMLElement(tag=str(direct_tag), type=html_element_type)
        html_elements.append(html_element)
    
    return html_elements

def get_title_meta_elements(raw_html: str, title: str):
    soup = default_html_parser(raw_html=raw_html)
    title_html_elements: list[BaseHTMLElement] = []

    for tag in soup.find_all("meta"):
        raw_tag = str(tag)
        pattern = re.compile(title)
        if bool(pattern.search(raw_tag)):
            title_html_element = BaseHTMLElement(tag=raw_tag, type=HTMLElementType.TITLE)
            title_html_elements.append(title_html_element)
    
    return title_html_elements


async def extract_elements(target_url: str, content: str, html_element_type: HTMLElementType):
    try:
        raw_html = await fetch_raw_html(target_url=target_url)
        insert_operations = []
        semaphore = asyncio.Semaphore(50)
        for element in get_html_elements_having_content(raw_html, content, html_element_type):
            insert_operations.append(insert_html_element(CreatingHTMLElement(**element.model_dump()), semaphore))
        await asyncio.gather(*insert_operations)
    except Exception as e:
        print(f"Failed to extract elements: {e}")