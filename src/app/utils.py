import magic


def guess_content_type(data: bytes):
    chunk = data[: 1024 * 4]
    mime_type = magic.from_buffer(chunk, mime=True)
    return mime_type or "application/octet-stream"
