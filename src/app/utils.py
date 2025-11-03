__all__ = ["guess_content_type", "getConfiguredStorage"]

import os
from enum import Enum

import magic

from .data_gateway import StorageProtocol
from .data_mapper.fs import FS
from .data_mapper.mem import Memory
from .data_mapper.s3 import S3


def guess_content_type(data: bytes):
    chunk = data[: 1024 * 4]
    mime_type = magic.from_buffer(chunk, mime=True)
    return mime_type or "application/octet-stream"


class StorageEnum(str, Enum):
    FS = "FS"
    S3 = "S3"
    MEMORY = "MEMORY"


def getConfiguredStorage() -> StorageProtocol:
    storage_type = StorageEnum(os.getenv("STORAGE", StorageEnum.S3.value))
    storages: dict[StorageEnum, StorageProtocol] = {
        StorageEnum.FS: FS,
        StorageEnum.S3: S3,
        StorageEnum.MEMORY: Memory,
    }
    return storages[storage_type]
