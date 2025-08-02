from celery_app import celery_app, EXTRACT_HTML_ELEMENTS_QUEUE
from celery_event_loop import celery_event_loop_manager
from .services import extract_elements
from .models import HTMLElementType

@celery_app.task(queue=EXTRACT_HTML_ELEMENTS_QUEUE)
def celery_extract_html_elements(target_url: str, content: str, html_element_type: str):
    celery_event_loop_manager.loop.run_until_complete(extract_elements(target_url, content, HTMLElementType(html_element_type)))