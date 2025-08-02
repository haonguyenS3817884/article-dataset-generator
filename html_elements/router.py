from fastapi import APIRouter
from common.models import APIResponse
from .tasks import celery_extract_html_elements
from .models import ExtractHTMLElementsRequestBody

router = APIRouter(
    prefix="/html-elements"
)

@router.post("/", response_model=APIResponse[str])
async def extract_html_elements(request_body: ExtractHTMLElementsRequestBody):
    celery_extract_html_elements.delay(request_body.target_url, request_body.content, request_body.html_element_type.value)
    return APIResponse(data="HTML Elements are extracting")