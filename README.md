# Static Server

I want to implement a configurable static server with a very simple API to store and retreive static resources.

It will be configurable to save data on the host file system or to save data to AWS S3.

## start

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r src/requirements-lock.txt

    fastapi dev src/main.py

    curl -X 'POST' \
      'http://127.0.0.1:8000/photos/products/23/PW-11004768_.png' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@PW-11004768_.png;type=image/png'

    curl -X 'GET' \
      'http://127.0.0.1:8000/photos/products/23/PW-11004768_.png' \
      -H 'accept: application/json'

## Docker

    docker build -t static-server:dev --build-arg USER_ID=`id -u` --build-arg GROUP_ID=`id -g` .
    docker run --rm -it -p 8000:8000 -v ./src/:/app static-server:dev
    docker images prune -a
