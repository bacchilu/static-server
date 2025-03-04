import os
from enum import Enum
from typing import IO, Protocol, runtime_checkable

from libs.fs import FS
from libs.s3 import S3


@runtime_checkable
class StorageProtocol(Protocol):
    async def get(self, key: str) -> bytes: ...

    async def upload(self, filename: str, file: IO[bytes], sub_path: str) -> str: ...

    async def delete(self, key: str) -> None: ...


class StorageEnum(str, Enum):
    FS = "FS"
    S3 = "S3"


STORAGE_TYPE = StorageEnum(os.getenv("STORAGE", "S3"))
storages: dict[StorageEnum, StorageProtocol] = {
    StorageEnum.FS: FS,
    StorageEnum.S3: S3,
}


def getStorage():
    return storages[STORAGE_TYPE]
