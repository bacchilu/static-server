import asyncio
import io

from dotenv import load_dotenv

from . import Bucket

load_dotenv()


S3_BUCKET = "life365"


async def go():
    async with Bucket.create_obj(S3_BUCKET) as bucket:
        with io.BytesIO(b"Nel mezzo del cammin di nostra vita") as fp:
            await bucket.upload_fileobj(fp, "TEST/test.py")
        with io.BytesIO() as fp:
            await bucket.download_fileobj(fp, "TEST/test.py")
            print(fp.getvalue())
        await bucket.delete_objects("TEST/test.py")


if __name__ == "__main__":
    asyncio.run(go())
