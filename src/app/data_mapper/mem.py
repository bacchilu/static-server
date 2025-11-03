__all__ = ["Memory"]

import os
from pathlib import Path
from typing import IO

from ..data_gateway import StorageProtocol

UPLOAD_DICT = {}


class Memory(StorageProtocol):
    @staticmethod
    async def get(key: str) -> bytes:
        p = Path(key)
        key, file_name = str(p.parent), p.name
        return UPLOAD_DICT[key][file_name]

    @staticmethod
    async def upload(filename: str, file: IO[bytes], sub_path: str) -> str:
        UPLOAD_DICT[sub_path] = UPLOAD_DICT.get(sub_path, {})
        UPLOAD_DICT[sub_path][filename] = file.read()
        return os.path.join(sub_path, filename)

    @staticmethod
    async def delete(key: str) -> None:
        p = Path(key)
        key, file_name = str(p.parent), p.name
        del UPLOAD_DICT[key][file_name]

    @staticmethod
    async def list_files(key: str) -> list[str]:
        return [os.path.join(key, f_name) for f_name in UPLOAD_DICT[key].keys()]
