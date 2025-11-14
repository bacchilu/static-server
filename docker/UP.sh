#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

create_directories() {
    mkdir -p $UPLOAD_DIRECTORY
}

ENVIRONMENT=$1

if [ "$ENVIRONMENT" == "DEV" ]; then
    create_directories
    docker compose --env-file .env up dev
elif [ "$ENVIRONMENT" == "PROD" ]; then
    create_directories
    docker compose --env-file .env up -d prod
else
    echo "Invalid environment specified: $ENVIRONMENT"
fi