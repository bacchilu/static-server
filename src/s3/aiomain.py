import asyncio
import io
import os

import aioboto3
from dotenv import load_dotenv


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


async def go():
    session = aioboto3.Session()
    async with session.resource("s3") as s3:
        bucket = await s3.Bucket("life365")
        with io.BytesIO(b"Nel mezzo del cammin di nostra vita") as fp:
            await bucket.upload_fileobj(fp, "TEST/test.py", {"ACL": "public-read"})
        with io.BytesIO() as fp:
            await bucket.download_fileobj("TEST/test.py", fp)
            print(fp.getvalue())
        await bucket.delete_objects(Delete={"Objects": [{"Key": "TEST/test.py"}]})


if __name__ == "__main__":
    asyncio.run(go())
