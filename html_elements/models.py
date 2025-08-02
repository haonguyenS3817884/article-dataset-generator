from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from enum import Enum
from datetime import datetime
from common.models import PyObjectId
from utils.convert_handler import encode_datetime
from utils.datetime_handler import utc_now

class HTMLElementType(Enum):
    TITLE = "title"
    PUBLISHED_DATE = "published_date"
    AUTHOR = "author"

def encode_html_element_type(html_element_type: HTMLElementType) -> str:
    return html_element_type.value

class BaseHTMLElement(BaseModel):
    tag: str
    type: HTMLElementType

class HTMLElement(BaseHTMLElement):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        validate_by_name = True,
        json_encoders = {ObjectId: str, datetime: encode_datetime}
    )

class CreatingHTMLElement(BaseHTMLElement):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    model_config = ConfigDict(
        json_encoders = {datetime: encode_datetime, HTMLElementType: encode_html_element_type}
    )

class ExtractHTMLElementsRequestBody(BaseModel):
    target_url: str
    content: str
    html_element_type: HTMLElementType