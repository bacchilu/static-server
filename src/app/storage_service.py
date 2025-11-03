__all__ = ["StorageService"]

import os
from pathlib import Path
from typing import IO

from .data_gateway import StorageProtocol


def check_key(key: str) -> str:
    key = key.strip()
    if len(key) == 0:
        raise Exception("Key cannot be empty.")
    if key.startswith("/"):
        raise Exception("Key cannot start with '/'.")
    if "." in key:
        raise Exception("Key cannot contain '.'.")
    if ".." in key:
        raise Exception("Key cannot contain '..'.")
    if "" in key.split("/"):
        raise Exception("Key cannot contain '//'.")
    return key


def check_path(file_path: str):
    p = Path(file_path)
    key, file_name = str(p.parent), p.name
    return os.path.join(check_key(key), file_name)


class StorageService:
    def __init__(self, storage: StorageProtocol):
        self.storage = storage

    async def upload_file(self, filename: str, file: IO[bytes], key: str) -> str:
        return await self.storage.upload(filename, file, check_key(key))

    async def get_file(self, file_path: str) -> bytes:
        return await self.storage.get(check_path(file_path))

    async def delete_file(self, file_path: str) -> None:
        await self.storage.delete(check_path(file_path))

    async def list_files(self, key: str) -> list[str]:
        return await self.storage.list_files(check_key(key))
