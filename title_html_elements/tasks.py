from celery_app import celery_app, EXTRACT_TITLE_HTML_ELEMENTS_QUEUE
from celery_event_loop import celery_event_loop_manager
from .services import extract_title_elements

@celery_app.task(queue=EXTRACT_TITLE_HTML_ELEMENTS_QUEUE)
def celery_extract_title_elements(target_url: str, article_title: str):
    celery_event_loop_manager.loop.run_until_complete(extract_title_elements(target_url, article_title))