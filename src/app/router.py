__all__ = ["router"]

import os

from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status

from .service import Service
from .utils import getConfiguredStorage, guess_content_type

storage = getConfiguredStorage()
service = Service(storage)


router = APIRouter()


@router.post("/{key:path}", status_code=status.HTTP_201_CREATED)
async def upload_file(response: Response, key: str, file: UploadFile = File(...)):
    assert file.filename is not None
    try:
        file_location = await service.upload_file(file.filename, file.file, key)
        response.headers["Location"] = file_location
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{key:path}/")
async def list_files(key: str):
    try:
        return await service.list_files(key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{key:path}/{filename}")
async def get_file(key: str, filename: str):
    try:
        file_data = await service.get_file(os.path.join(key, filename))
        return Response(
            file_data,
            media_type=guess_content_type(file_data),
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{key:path}")
async def delete_file_with_path(key: str):
    try:
        await service.delete_file(key)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
