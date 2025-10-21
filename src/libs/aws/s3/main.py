import io
import os

from dotenv import load_dotenv

from . import Bucket

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

S3_BUCKET = "life365"
REGION_NAME = "eu-central-1"


if __name__ == "__main__":
    bucket = Bucket.create_obj(
        S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME
    )
    with io.BytesIO(b"Nel mezzo del cammin di nostra vita") as fp:
        bucket.upload_fileobj(fp, "TEST/test.py")
    with io.BytesIO() as fp:
        bucket.download_fileobj("TEST/test.py", fp)
        print(fp.getvalue())
    print(list(bucket.list_files("TEST")))
    bucket.delete_objects("TEST/test.py")
