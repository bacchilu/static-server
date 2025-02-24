import os
from typing import IO


UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "/tmp")


async def get(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.isfile(file_path):
        raise Exception("File not found")
    with open(file_path, "rb") as fp:
        return fp.read()


async def upload(filename: str, file: IO[bytes], sub_path: str):
    target_directory = os.path.join(UPLOAD_DIRECTORY, sub_path)
    os.makedirs(target_directory, exist_ok=True)

    file_location = os.path.join(target_directory, filename)
    with open(file_location, "wb") as fp:
        fp.write(file.read())
    return file_location


async def delete(key: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, key)
    os.remove(file_path)
