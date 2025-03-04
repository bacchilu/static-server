import io
from typing import IO

from aws.aios3 import Bucket


class S3:
    @staticmethod
    async def get(key: str):
        async with Bucket.create_obj("life365") as bucket:
            with io.BytesIO() as fp:
                await bucket.download_fileobj(fp, key)
                return fp.getvalue()

    @staticmethod
    async def upload(filename: str, file: IO[bytes], sub_path: str):
        async with Bucket.create_obj("life365") as bucket:
            file.seek(0)
            await bucket.upload_fileobj(file, f"{sub_path}/{filename}")
            return (
                f"https://life365.s3.eu-central-1.amazonaws.com/{sub_path}/{filename}"
            )

    @staticmethod
    async def delete(key: str):
        async with Bucket.create_obj("life365") as bucket:
            await bucket.delete_objects(key)
