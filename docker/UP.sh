#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

ENVIRONMENT=$1

if [ "$ENVIRONMENT" == "DEV" ]; then
    docker compose --env-file .env up dev
elif [ "$ENVIRONMENT" == "PROD" ]; then
    docker compose --env-file .env up -d prod
else
    echo "Invalid environment specified: $ENVIRONMENT"
fi