from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from core.database import db
import os

router = APIRouter()

@router.get("/watch/{file_id}")
async def stream_file(file_id: str, request: Request):

    file = await db.files.find_one({"file_id": file_id})
    if not file:
        raise HTTPException(404)

    path = file["path"]
    file_size = os.path.getsize(path)

    return StreamingResponse(
        open(path, "rb"),
        media_type=file["mime_type"]
    )
