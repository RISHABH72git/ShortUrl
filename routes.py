import random
import string
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse, JSONResponse

from model import BaseResponse
from redis_config import get_redis_client

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/url/short")
async def url_short(long_url: str, request: Request):
    # Random uppercase letter
    random_chars = ''.join(random.choices(string.ascii_uppercase, k=3))
    # Random lowercase letter
    random_lower = ''.join(random.choices(string.ascii_lowercase, k=3))
    url_id = f"{long_url[-1]}{random_chars}{random_lower}{long_url[0]}"
    redis_client = get_redis_client()
    if not await redis_client.exists(url_id):
        await redis_client.set(url_id, long_url)

    host = str(request.base_url)
    short_url = f"{host}{url_id}"
    return BaseResponse(message="short url created", data={"short_url": short_url, "original_url": long_url})


@router.get("/{unique_id}", response_model=BaseResponse)
async def parse_url(unique_id: str):
    redis_client = get_redis_client()
    value = await redis_client.get(unique_id)
    print(value)
    if value is None:
        return JSONResponse(
            status_code=404,
            content=BaseResponse(
                message="Short URL not found",
                data={"id": unique_id}
            ).dict())

    return RedirectResponse(url=value)
