import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()


UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "/tmp")


async def save_file(file: UploadFile, sub_path: str):
    assert file.filename is not None

    target_directory = os.path.join(UPLOAD_DIRECTORY, sub_path)
    os.makedirs(target_directory, exist_ok=True)

    file_location = os.path.join(target_directory, file.filename)
    with open(file_location, "wb") as fp:
        content = await file.read()
        fp.write(content)
    return file_location


@app.post("/{sub_path:path}")
async def upload_file(sub_path: str = "", file: UploadFile = File(...)):
    if ".." in sub_path or sub_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid sub-path")
    file_location = await save_file(file, sub_path)
    return {"filename": file.filename, "location": file_location}


@app.get("/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@app.get("/{sub_path:path}/{filename}")
async def get_file_with_path(sub_path: str, filename: str):
    if ".." in sub_path or sub_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid sub-path")
    file_path = os.path.join(UPLOAD_DIRECTORY, sub_path, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
