# Static Server

I want to implement a configurable static server with a very simple API to store and retreive static resources.

It will be configurable to save data on the host file system or to save data to AWS S3.

The current latest version is [`static-server:3.0.5`](https://hub.docker.com/r/bacchilu/static-server).

## start (dev mod)

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r requirements-lock.txt

    export $(grep -v '^#' docker/.env | xargs)
    fastapi dev src/main.py

## sample requests

    curl -X 'POST' \
    'http://0.0.0.0:8000/xxx/yyy/dante.txt' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@KEN2025_ticket_31275276.pdf;type=application/pdf'

    curl -X 'DELETE' \
    'http://0.0.0.0:8000/xxx%2FKEN2025_ticket_31275276.pdf' \
    -H 'accept: application/json'

## Docker

### Deploy to Docker Hub

    cd docker
    source DOCKER_HUB.sh

### dev

    cd docker
    source PREPARE.sh
    docker compose up dev

or

    python3 -m venv ENV
    source ENV/bin/activate
    pip3 install -r requirements.txt
    fastapi dev src/main.py --host 0.0.0.0

### prod

    cd docker
    source PREPARE.sh
    docker compose up -d prod

### clear

    cd docker
    docker compose down

## S3

    cd src/libs/aws
    python3 -m venv ENV
    source ENV/bin/activate

    pip3 install -r s3/requirements.txt
    python3 -m s3.main

    pip3 install -r aios3/requirements.txt
    python3 -m aios3.main
