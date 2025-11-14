__all__ = ["router"]

from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status

from .storage_service import StorageService
from .utils import getConfiguredStorage, guess_content_type

storage = getConfiguredStorage()
storage_service = StorageService(storage)


router = APIRouter()


@router.post("/{key:path}/{filename}", status_code=status.HTTP_201_CREATED)
async def upload_file(
    response: Response, key: str, filename: str, file: UploadFile = File(...)
):
    try:
        file_location = await storage_service.upload_file(filename, file.file, key)
        response.headers["Location"] = file_location
        return {"filename": filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{key:path}/")
async def list_files(key: str):
    try:
        return await storage_service.list_files(key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{key:path}")
async def get_file(key: str):
    try:
        file_data = await storage_service.get_file(key)
        return Response(
            file_data,
            media_type=guess_content_type(file_data),
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{key:path}")
async def delete_file_with_path(key: str):
    try:
        await storage_service.delete_file(key)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
