from pydantic import BaseModel, HttpUrl


class BaseResponse(BaseModel):
    message: str
    data: dict
