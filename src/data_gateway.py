from typing import IO, Protocol, runtime_checkable


@runtime_checkable
class StorageProtocol(Protocol):
    @staticmethod
    async def get(key: str) -> bytes: ...

    @staticmethod
    async def upload(filename: str, file: IO[bytes], sub_path: str) -> str: ...

    @staticmethod
    async def delete(key: str) -> None: ...

    @staticmethod
    async def list_files(key: str) -> list[str]: ...
