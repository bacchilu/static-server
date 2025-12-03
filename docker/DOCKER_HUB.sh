#!/bin/bash

TAG=3.0.6

docker build -t bacchilu/static-server -t bacchilu/static-server:$TAG -f ./Dockerfile ..
docker push bacchilu/static-server
docker push bacchilu/static-server:$TAG
docker image prune -af
