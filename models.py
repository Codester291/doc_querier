from pydantic import BaseModel

class ResponseModel(BaseModel):
    code: str
    message: str
    data: dict = {}

class QueryDTO(BaseModel):
    url: str
    query: str