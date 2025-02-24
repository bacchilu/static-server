import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response

from libs import fs, s3
from libs.utils import guess_content_type, check_key


app = FastAPI()


@app.post("/{key:path}")
async def upload_file(key: str, file: UploadFile = File(...)):
    assert file.filename is not None
    try:
        key = check_key(key)
        file_location = await fs.upload(file.filename, file.file, key)
        file_location = await s3.upload(file.filename, file.file, key)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/{key:path}/{filename}")
async def get_file(key: str, filename: str):
    try:
        key = check_key(key)
        file_data = await fs.get(os.path.join(key, filename))
        file_data = await s3.get(os.path.join(key, filename))
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
    await fs.delete(key)
    await s3.delete(key)
    return {"filename": key}
