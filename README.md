# Static Server

Static Server is a small FastAPI service to manage static resources: you POST a file to a path and it is persisted by the selected storage provider; later you GET or DELETE the same path to retrieve or remove it. The API keeps the paths stable while letting you swap where the bytes actually live.

Three storage providers are supported:
- MEMORY: stores uploads in an in-memory dictionary; great for local demos, non-persistent.
- FS: writes files to the host file system under `UPLOAD_DIRECTORY`; survives restarts as long as the volume persists.
- S3: streams objects to an AWS S3 bucket using provided credentials/region; returned URLs point to the bucket.

The current latest version is [`bacchilu/static-server:3.0.5`](https://hub.docker.com/r/bacchilu/static-server).

## Configuration (.env)

Set environment variables to pick and configure storage:
- `STORAGE` = `MEMORY` | `FS` | `S3`.
- FS: set `UPLOAD_DIRECTORY` to a writable path (e.g., `/tmp/uploads` or a mounted volume).
- S3: set `S3_BUCKET`, `REGION_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`; ensure the IAM principal can upload/list/delete objects. Returned URLs use `https://<bucket>.s3.<region>.amazonaws.com/...`.

## API

Routes are relative to `/`:
- `POST /{key:path}/{filename}` — multipart upload (`file` field). Saves under `{key}/{filename}`, sets `Location` header, returns JSON with `location` and `file_path`.
- `GET /{key:path}/` — lists files directly under `{key}`.
- `GET /{key:path}` — downloads the file at `{key}`; media type is guessed from bytes.
- `DELETE /{key:path}` — deletes the file at `{key}`.

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

## Running from Docker Hub

    docker run --env-file docker/.env -p 8000:8000 bacchilu/static-server:3.0.5
