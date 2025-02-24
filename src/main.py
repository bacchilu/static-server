import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, Response

from aws.aios3 import Bucket

app = FastAPI()


class FS:
    UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "/tmp")

    @staticmethod
    async def get_path(filename: str):
        file_path = os.path.join(FS.UPLOAD_DIRECTORY, filename)
        if not os.path.isfile(file_path):
            raise Exception("File not found")
        with open(file_path, "rb") as fp:
            return fp.read()

    @staticmethod
    async def upload(file: UploadFile, sub_path: str):
        assert file.filename is not None

        target_directory = os.path.join(FS.UPLOAD_DIRECTORY, sub_path)
        os.makedirs(target_directory, exist_ok=True)

        file_location = os.path.join(target_directory, file.filename)
        with open(file_location, "wb") as fp:
            content = await file.read()
            fp.write(content)
        return file_location

    @staticmethod
    async def delete(key: str):
        file_path = os.path.join(FS.UPLOAD_DIRECTORY, key)
        os.remove(file_path)


class S3:
    @staticmethod
    async def get(key: str):
        import io

        async with Bucket.create_obj("life365") as bucket:
            with io.BytesIO() as fp:
                await bucket.download_fileobj(fp, key)
                return fp.getvalue()

    @staticmethod
    async def upload(file: UploadFile, sub_path: str):
        assert file.filename is not None

        async with Bucket.create_obj("life365") as bucket:
            file.file.seek(0)
            await bucket.upload_fileobj(file.file, f"{sub_path}/{file.filename}")
            return f"https://life365.s3.eu-central-1.amazonaws.com/{sub_path}/{file.filename}"

    @staticmethod
    async def delete(key: str):
        async with Bucket.create_obj("life365") as bucket:
            await bucket.delete_objects(key)


def check_key(key: str):
    key = key.strip()
    if len(key) == 0:
        raise Exception("Sub-path cannot be empty.")
    if key.startswith("/"):
        raise Exception("Sub-path cannot start with '/'.")
    if "." in key:
        raise Exception("Sub-path cannot contain '.'.")
    if ".." in key:
        raise Exception("Sub-path cannot contain '..'.")
    if "" in key.split("/"):
        raise Exception("Sub-path cannot contain '//'.")
    return key


@app.post("/{key:path}")
async def upload_file(key: str, file: UploadFile = File(...)):
    try:
        key = check_key(key)
        file_location = await FS.upload(file, key)
        await S3.upload(file, key)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/{key:path}/{filename}")
async def get_file(key: str, filename: str):
    try:
        key = check_key(key)
        file = await FS.get_path(os.path.join(key, filename))
        file = await S3.get(os.path.join(key, filename))
        return Response(
            file,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/{key:path}")
async def delete_file_with_path(key: str):
    if ".." in key or key.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid sub-path")
    await FS.delete(key)
    await S3.delete(key)
    return {"filename": key}
