from boto3.session import Session
from mypy_boto3_s3.service_resource import _Bucket


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
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="eu-central-1",
        )
        self.s3 = session.resource("s3")

    def all(self):
        return (Bucket(b) for b in self.s3.buckets.all())

    def get_bucket(self, name: str):
        return Bucket(self.s3.Bucket(name))
