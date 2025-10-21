from typing import IO, Protocol, runtime_checkable

from .data_gateway import StorageProtocol


@runtime_checkable
class ApplicationProtocol(Protocol):
    async def upload_file(
        self, filename: str, file: IO[bytes], sub_path: str
    ) -> str: ...

    async def get_file(self, key: str) -> bytes: ...

    async def delete_file(self, key: str) -> None: ...

    async def list_files(self, key: str) -> list[str]: ...


def check_key(key: str):
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


class Application(ApplicationProtocol):
    def __init__(self, storage: StorageProtocol):
        self.storage = storage

    async def upload_file(self, filename: str, file: IO[bytes], sub_path: str) -> str:
        sub_path = check_key(sub_path)
        return await self.storage.upload(filename, file, sub_path)

    async def get_file(self, key: str) -> bytes:
        if ".." in key or key.startswith("/"):
            raise Exception("Invalid key")
        return await self.storage.get(key)

    async def delete_file(self, key: str) -> None:
        if ".." in key or key.startswith("/"):
            raise Exception("Invalid key")
        await self.storage.delete(key)

    async def list_files(self, key: str) -> list[str]:
        if ".." in key or key.startswith("/"):
            raise Exception("Invalid key")
        return await self.storage.list_files(key)
