from contextlib import asynccontextmanager
from typing import IO

import aioboto3
import magic


def guess_content_type(file_obj: IO[bytes]):
    current_pos = file_obj.tell()
    chunk = file_obj.read(4096)
    file_obj.seek(current_pos)
    mime_type = magic.from_buffer(chunk, mime=True)
    return mime_type or "application/octet-stream"


class Bucket:
    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    @asynccontextmanager
    async def create_obj(
        cls, name: str, aws_access_key_id: str, aws_secret_access_key: str
    ):
        session = aioboto3.Session(region_name="eu-central-1")
        async with session.resource("s3") as s3:
            bucket = await s3.Bucket(name)
            yield cls(bucket)

    async def upload_fileobj(self, fp: IO[bytes], key: str):
        await self.bucket.upload_fileobj(
            fp, key, {"ACL": "public-read", "ContentType": guess_content_type(fp)}
        )

    async def download_fileobj(self, fp: IO[bytes], key: str):
        await self.bucket.download_fileobj(key, fp)

    async def delete_objects(self, key: str):
        await self.bucket.delete_objects(Delete={"Objects": [{"Key": key}]})
