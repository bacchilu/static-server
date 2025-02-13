import io

from .s3 import Bucket


if __name__ == "__main__":
    bucket = Bucket.create_obj("life365")
    with io.BytesIO(b"Nel mezzo del cammin di nostra vita") as fp:
        bucket.upload_fileobj(fp, "TEST/test.py")
    with io.BytesIO() as fp:
        bucket.download_fileobj("TEST/test.py", fp)
        print(fp.getvalue())
    bucket.delete_objects("TEST/test.py")
