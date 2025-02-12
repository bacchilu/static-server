from dotenv import load_dotenv
from typing import IO
import os

from boto3.session import Session
import magic
from mypy_boto3_s3.service_resource import _Bucket


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


def guess_content_type(file_obj: IO[bytes]):
    current_pos = file_obj.tell()
    chunk = file_obj.read(4096)
    file_obj.seek(current_pos)
    mime_type = magic.from_buffer(chunk, mime=True)
    return mime_type or "application/octet-stream"


class Bucket:
    def __init__(self, bucket: _Bucket):
        self.bucket = bucket

    @classmethod
    def create_obj(cls, name: str):
        session = Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="eu-central-1",
        )
        s3 = session.resource("s3")
        return Bucket(s3.Bucket(name))

    def upload_fileobj(self, fp: IO[bytes], key: str):
        extraArgs = {"ACL": "public-read", "ContentType": guess_content_type(fp)}
        self.bucket.upload_fileobj(fp, key, extraArgs)

    def delete_objects(self, key: str):
        self.bucket.delete_objects(Delete={"Objects": [{"Key": key}]})

    def download_fileobj(self, key: str, fp: IO[bytes]):
        self.bucket.download_fileobj(key, fp)

    def __str__(self):
        return f"<Bucket name={self.bucket.name}>"


class S3:
    def __init__(self):
        session = Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="eu-central-1",
        )
        self.s3 = session.resource("s3")

    def all(self):
        return (Bucket(b) for b in self.s3.buckets.all())

    def get_bucket(self, name: str):
        return Bucket(self.s3.Bucket(name))
