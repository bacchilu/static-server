# Static Server

I want to implement a configurable static server with a very simple API to store and retreive static resources.

It will be configurable to save data on the host file system or to save data to AWS S3.

## start (dev mod)

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r src/requirements-lock.txt

    export $(grep -v '^#' docker/.env | xargs)
    fastapi dev src/main.py

    curl -X 'POST' \
    'http://0.0.0.0:8000/xxx' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@KEN2025_ticket_31275276.pdf;type=application/pdf'

    curl -X 'DELETE' \
    'http://0.0.0.0:8000/xxx%2FKEN2025_ticket_31275276.pdf' \
    -H 'accept: application/json'

## Docker

    docker build -t static-server -f ./docker/Dockerfile .

### dev

    docker run --rm -it -p 8000:8000 --env-file docker/.env static-server fastapi dev main.py --host 0.0.0.0

### prod

    docker run --rm -it -p 80:8000 --env-file docker/.env static-server

### clear

    docker image prune -a

---

    source UP.sh [DEV | PROD]
    source DOWN.sh

## S3

    pip3 install -r src/aws/s3/requirements.txt
    python3 -m src.aws.s3.main

    pip3 install -r src/aws/aios3/requirements.txt
    python3 -m src.aws.aios3.main
