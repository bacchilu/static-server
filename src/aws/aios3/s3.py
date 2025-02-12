from contextlib import asynccontextmanager
import io
import os

import aioboto3
from dotenv import load_dotenv


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


class Bucket:
    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    @asynccontextmanager
    async def create_obj(cls, name: str):
        session = aioboto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="eu-central-1",
        )
        async with session.resource("s3") as s3:
            bucket = await s3.Bucket(name)
            yield cls(bucket)

    async def upload_fileobj(self, fp: io.BytesIO, key: str):
        await self.bucket.upload_fileobj(fp, key, {"ACL": "public-read"})

    async def download_fileobj(self, fp: io.BytesIO, key: str):
        await self.bucket.download_fileobj(key, fp)

    async def delete_objects(self, key: str):
        await self.bucket.delete_objects(Delete={"Objects": [{"Key": key}]})
