# Static Server

I want to implement a configurable static server with a very simple API to store and retreive static resources.

It will be configurable to save data on the host file system or to save data to AWS S3.

## start

    fastapi dev main.py

    curl -X 'POST' \
      'http://127.0.0.1:8000/photos/products/23/PW-11004768_.png' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@PW-11004768_.png;type=image/png'

    curl -X 'GET' \
      'http://127.0.0.1:8000/photos/products/23/PW-11004768_.png' \
      -H 'accept: application/json'
