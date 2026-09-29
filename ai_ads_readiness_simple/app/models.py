from pydantic import BaseModel, Field, HttpUrl
class AnalyzeRequest(BaseModel):
    url: HttpUrl
    max_pages: int=Field(default=10,ge=1,le=25)
