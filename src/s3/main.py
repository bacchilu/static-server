import io
import os

from dotenv import load_dotenv

from .s3 import S3


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


if __name__ == "__main__":
    s3 = S3(
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print(list(s3.all()))

    bucket = s3.get_bucket("life365")
    with io.BytesIO(b"Nel mezzo del cammin di nostra vita") as fp:
        bucket.upload_fileobj(fp, "plain/text", "TEST/test.py")
    bucket.delete_objects("TEST/test.py")
