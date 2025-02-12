import io
import os
import random

from dotenv import load_dotenv

from .s3 import S3


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


def rand_open():
    return random.choice(
        (
            io.BytesIO(b"Nel mezzo del cammin di nostra vita"),
            open("src/aws/s3/main.py", "rb"),
        )
    )


if __name__ == "__main__":
    s3 = S3(
        aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print(list(s3.all()))

    bucket = s3.get_bucket("life365")
    with rand_open() as fp:
        bucket.upload_fileobj(fp, "TEST/test.py")
    with io.BytesIO() as fp:
        bucket.download_fileobj("TEST/test.py", fp)
        print(fp.getvalue())
    bucket.delete_objects("TEST/test.py")
