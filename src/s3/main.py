import os

from boto3.session import Session
from mypy_boto3_s3.service_resource import _Bucket
from dotenv import load_dotenv


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class Bucket:
    def __init__(self, bucket: _Bucket):
        self.bucket = bucket

    def upload_fileobj(self, file: str, content_type: str, key: str):
        with open(file, "rb") as fp:
            extraArgs = {"ACL": "public-read", "ContentType": content_type}
            self.bucket.upload_fileobj(fp, key, extraArgs)

    def delete_objects(self, key: str):
        self.bucket.delete_objects(Delete={"Objects": [{"Key": key}]})

    def __str__(self):
        return f"<Bucket name={self.bucket.name}>"


class S3:
    def __init__(self, session: Session):
        self.s3 = session.resource("s3")

    def all(self):
        return (Bucket(b) for b in self.s3.buckets.all())

    def get_bucket(self, name: str):
        return Bucket(self.s3.Bucket(name))


if __name__ == "__main__":
    session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="eu-west-1",
    )
    s3 = S3(session)

    print(list(s3.all()))

    bucket = s3.get_bucket("life365")
    bucket.upload_fileobj("main.py", "plain/text", "TEST/test.py")
    bucket.delete_objects("TEST/test.py")
