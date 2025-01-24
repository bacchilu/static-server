import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from s3.s3 import S3

app = FastAPI()


UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "/tmp")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


async def save_to_disk(file: UploadFile, sub_path: str):
    assert file.filename is not None

    target_directory = os.path.join(UPLOAD_DIRECTORY, sub_path)
    os.makedirs(target_directory, exist_ok=True)

    file_location = os.path.join(target_directory, file.filename)
    with open(file_location, "wb") as fp:
        content = await file.read()
        fp.write(content)
    return file_location


def save_to_s3(file: UploadFile, sub_path: str):
    assert file.filename is not None

    s3 = S3(
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    bucket = s3.get_bucket("life365")
    file.file.seek(0)
    bucket.upload_fileobj(file.file, f"{sub_path}/{file.filename}")
    return f"https://life365.s3.eu-central-1.amazonaws.com/{sub_path}/{file.filename}"


@app.post("/{sub_path:path}")
async def upload_file(sub_path: str = "", file: UploadFile = File(...)):
    if ".." in sub_path or sub_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid sub-path")
    file_location = await save_to_disk(file, sub_path)
    save_to_s3(file, sub_path)
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
