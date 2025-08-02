import asyncio
from database import db_manager
from config.constants import HTML_ELEMENTS_COLLECTIONS
from .models import CreatingHTMLElement

html_elements_collection = db_manager.db[HTML_ELEMENTS_COLLECTIONS]

async def insert_html_element(payload: CreatingHTMLElement, concurrency_level: asyncio.Semaphore):
    try:
        async with concurrency_level:
            payload_dict = payload.model_dump(mode="json")
            await html_elements_collection.insert_one(payload_dict)
            print(f"{payload.tag} is inserted")
    except Exception as e:
        print(f"Failed to insert html element: {e}")