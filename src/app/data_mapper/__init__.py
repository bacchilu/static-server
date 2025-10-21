import os
from enum import Enum

from ..data_gateway import StorageProtocol
from .fs import FS
from .s3 import S3


class StorageEnum(str, Enum):
    FS = "FS"
    S3 = "S3"


def getStorage() -> StorageProtocol:
    STORAGE_TYPE = StorageEnum(os.getenv("STORAGE", "S3"))
    storages: dict[StorageEnum, StorageProtocol] = {
        StorageEnum.FS: FS,
        StorageEnum.S3: S3,
    }

    return storages[STORAGE_TYPE]
