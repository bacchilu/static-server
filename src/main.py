import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

from get_storage import getStorage
from interactor import Application
from utils import guess_content_type

application = Application(getStorage())

engine = FastAPI()


@engine.post("/{key:path}")
async def upload_file(key: str, file: UploadFile = File(...)):
    assert file.filename is not None
    try:
        file_location = await application.upload_file(file.filename, file.file, key)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@engine.get("/{key:path}/{filename}")
async def get_file(key: str, filename: str):
    try:
        file_data = await application.get_file(os.path.join(key, filename))
        return Response(
            file_data,
            media_type=guess_content_type(file_data),
            # headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@engine.delete("/{key:path}")
async def delete_file_with_path(key: str):
    try:
        await application.delete_file(key)
        return {"filename": key}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
