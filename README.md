# Static Server

I want to implement a configurable static server with a very simple API to store and retreive static resources.

It will be configurable to save data on the host file system or to save data to AWS S3.

[DockerHub](https://hub.docker.com/r/bacchilu/static-server)

## start (dev mod)

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r src/app/requirements-lock.txt

    export $(grep -v '^#' docker/.env | xargs)
    fastapi dev src/app/main.py

## sample requests

    curl -X 'POST' \
    'http://0.0.0.0:8000/xxx' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@KEN2025_ticket_31275276.pdf;type=application/pdf'

    curl -X 'DELETE' \
    'http://0.0.0.0:8000/xxx%2FKEN2025_ticket_31275276.pdf' \
    -H 'accept: application/json'

## Docker

### Deploy

    docker build -t bacchilu/static-server -t bacchilu/static-server:3.0.0 -f ./docker/Dockerfile .
    docker push bacchilu/static-server
    docker push bacchilu/static-server:3.0.0

### dev

    docker run --rm -it -p 8000:8000 --env-file docker/.env bacchilu/static-server fastapi dev app/main.py --host 0.0.0.0

or

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r src/app/requirements.txt
    fastapi dev src/app/main.py --host 0.0.0.0

### prod

    docker run --rm -it -p 80:8000 --env-file docker/.env bacchilu/static-server

### clear

    source UP.sh [DEV | PROD]
    source DOWN.sh

## S3
    cd src/libs/aws
    python3 -m venv ENV
    source ENV/bin/activate

    pip3 install -r s3/requirements.txt
    python3 -m s3.main

    pip3 install -r aios3/requirements.txt
    python3 -m aios3.main

## TODO

- File System Storage
- Better Bucket management
- JWT Authentication
