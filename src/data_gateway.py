from typing import IO, Protocol, runtime_checkable


@runtime_checkable
class StorageProtocol(Protocol):
    async def get(self, key: str) -> bytes: ...

    async def upload(self, filename: str, file: IO[bytes], sub_path: str) -> str: ...

    async def delete(self, key: str) -> None: ...
