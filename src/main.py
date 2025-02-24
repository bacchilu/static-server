from enum import Enum
import os
from typing import IO

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response

from libs import fs, s3
from libs.utils import guess_content_type, check_key


class StorageEnum(str, Enum):
    FS = "FS"
    S3 = "S3"


STORAGE = StorageEnum(os.getenv("STORAGE", "S3"))


app = FastAPI()


async def upload(filename: str, file: IO[bytes], key: str):
    if STORAGE == StorageEnum.FS:
        return await fs.upload(filename, file, key)
    if STORAGE == StorageEnum.S3:
        return await s3.upload(filename, file, key)
    assert False


async def get(key: str):
    if STORAGE == StorageEnum.FS:
        return await fs.get(key)
    if STORAGE == StorageEnum.S3:
        return await s3.get(key)
    assert False


async def delete(key: str):
    if STORAGE == StorageEnum.FS:
        await fs.delete(key)
    if STORAGE == StorageEnum.S3:
        await s3.delete(key)
    assert False


@app.post("/{key:path}")
async def upload_file(key: str, file: UploadFile = File(...)):
    assert file.filename is not None
    try:
        key = check_key(key)
        file_location = await upload(file.filename, file.file, key)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/{key:path}/{filename}")
async def get_file(key: str, filename: str):
    try:
        key = check_key(key)
        file_data = await get(os.path.join(key, filename))
        return Response(
            file_data,
            media_type=guess_content_type(file_data),
            # headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/{key:path}")
async def delete_file_with_path(key: str):
    if ".." in key or key.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid sub-path")
    await delete(key)
    await delete(key)
    return {"filename": key}
