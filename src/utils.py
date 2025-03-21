import magic


def guess_content_type(data: bytes):
    chunk = data[: 1024 * 4]
    mime_type = magic.from_buffer(chunk, mime=True)
    return mime_type or "application/octet-stream"


def check_key(key: str):
    key = key.strip()
    if len(key) == 0:
        raise Exception("Sub-path cannot be empty.")
    if key.startswith("/"):
        raise Exception("Sub-path cannot start with '/'.")
    if "." in key:
        raise Exception("Sub-path cannot contain '.'.")
    if ".." in key:
        raise Exception("Sub-path cannot contain '..'.")
    if "" in key.split("/"):
        raise Exception("Sub-path cannot contain '//'.")
    return key
