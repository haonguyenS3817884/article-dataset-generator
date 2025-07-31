from fastapi import APIRouter
from common.models import APIResponse
from .tasks import celery_extract_title_elements
from .models import ExtractTitleHTMLElementsRequestBody

router = APIRouter(
    prefix="/title-html-elements"
)

@router.post("/", response_model=APIResponse[str])
async def extract_title_html_elements(request_body: ExtractTitleHTMLElementsRequestBody):
    celery_extract_title_elements.delay(request_body.target_url, request_body.article_title)
    return APIResponse(data="Title HTML Elements are extracting")