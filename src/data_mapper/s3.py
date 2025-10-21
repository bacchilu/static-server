import io
import os
from typing import IO

from data_gateway import StorageProtocol
from libs.aws.aios3 import Bucket

S3_BUCKET = os.getenv("S3_BUCKET", "life365")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "XXXXXXXXXXXXXXXXXXXX")
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY", "YYYYYYYY+ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
)
REGION_NAME = os.getenv("REGION_NAME", "eu-central-1")


def get_bucket():
    return Bucket.create_obj(
        S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME
    )


class S3(StorageProtocol):
    @staticmethod
    async def get(key: str) -> bytes:
        async with get_bucket() as bucket:
            with io.BytesIO() as fp:
                await bucket.download_fileobj(fp, key)
                return fp.getvalue()

    @staticmethod
    async def upload(filename: str, file: IO[bytes], sub_path: str):
        async with get_bucket() as bucket:
            file.seek(0)
            await bucket.upload_fileobj(file, f"{sub_path}/{filename}")
            return f"https://{S3_BUCKET}.s3.eu-central-1.amazonaws.com/{sub_path}/{filename}"

    @staticmethod
    async def delete(key: str):
        async with get_bucket() as bucket:
            await bucket.delete_objects(key)

    @staticmethod
    async def list_files(key: str) -> list[str]:
        async with get_bucket() as bucket:
            return await bucket.list_files(key)
