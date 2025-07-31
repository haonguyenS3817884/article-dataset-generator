import asyncio
from database import db_manager
from config.constants import TITLE_HTML_ELEMENTS_COLLECTIONS
from .models import CreatingTitleHTMLElement

title_html_elements_collection = db_manager.db[TITLE_HTML_ELEMENTS_COLLECTIONS]

async def insert_title_html_element(payload: CreatingTitleHTMLElement, concurrency_level: asyncio.Semaphore):
    try:
        async with concurrency_level:
            payload_dict = payload.model_dump()
            await title_html_elements_collection.insert_one(payload_dict)
            print(f"{payload.tag_name} is inserted")
    except Exception as e:
        print(f"Failed to insert title html element: {e}")