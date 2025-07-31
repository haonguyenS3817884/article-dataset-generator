from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import Optional
from datetime import datetime
from common.models import PyObjectId, BaseHTMLElement
from utils.convert_handler import encode_datetime
from utils.datetime_handler import utc_now

class BaseTitleHTMLElement(BaseHTMLElement):
    name: Optional[str] = None
    property: Optional[str] = None

class TitleHTMLElement(BaseTitleHTMLElement):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        validate_by_name = True,
        json_encoders = {ObjectId: str, datetime: encode_datetime}
    )

class CreatingTitleHTMLElement(BaseTitleHTMLElement):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class ExtractTitleHTMLElementsRequestBody(BaseModel):
    target_url: str
    article_title: str