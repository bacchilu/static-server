from typing import IO, Protocol, runtime_checkable

from data_gateway import StorageProtocol


@runtime_checkable
class ApplicationProtocol(Protocol):
    async def get_file(self, key: str) -> bytes: ...

    async def upload_file(
        self, filename: str, file: IO[bytes], sub_path: str
    ) -> str: ...

    async def delete_file(self, key: str) -> None: ...


class Application(ApplicationProtocol):
    def __init__(self, storage: StorageProtocol):
        self.storage = storage

    async def get_file(self, key: str) -> bytes:
        return await self.storage.get(key)

    async def upload_file(self, filename: str, file: IO[bytes], sub_path: str) -> str:
        return await self.storage.upload(filename, file, sub_path)

    async def delete_file(self, key: str) -> None:
        await self.storage.delete(key)
