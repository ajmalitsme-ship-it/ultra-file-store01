import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

from core.database import db

router = APIRouter()


# =====================================
# File Streaming (Range Supported)
# =====================================
@router.get("/watch/{file_id}")
async def stream_file(file_id: str, request: Request):

    file = await db.files.find_one({"file_id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    path = file["path"]

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File missing on server")

    file_size = os.path.getsize(path)
    range_header = request.headers.get("range")

    start = 0
    end = file_size - 1

    if range_header:
        range_value = range_header.replace("bytes=", "")
        start_str, end_str = range_value.split("-")
        start = int(start_str)
        if end_str:
            end = int(end_str)

    def file_iterator():
        with open(path, "rb") as f:
            f.seek(start)
            yield f.read(end - start + 1)

    # Increment download counter
    await db.files.update_one(
        {"file_id": file_id},
        {"$inc": {"downloads": 1}}
    )

    return StreamingResponse(
        file_iterator(),
        media_type=file["mime_type"],
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
        }
    )


# =====================================
# Batch Viewer API
# =====================================
@router.get("/batch/{batch_id}")
async def get_batch(batch_id: str):

    batch = await db.batches.find_one({"batch_id": batch_id})
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    files_data = []

    for file_id in batch["files"]:
        file = await db.files.find_one({"file_id": file_id})
        if file:
            files_data.append({
                "file_id": file["file_id"],
                "file_name": file["file_name"],
                "size": file["file_size"],
                "downloads": file.get("downloads", 0)
            })

    return JSONResponse(content={
        "batch_id": batch_id,
        "total_files": len(files_data),
        "files": files_data
    })
