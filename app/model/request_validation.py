from pydantic import BaseModel, Field


class ScrapeRequestModel(BaseModel):
    url: str
    page: int = Field(..., ge=1, le=99999)

