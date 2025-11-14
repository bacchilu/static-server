#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
source .env
mkdir -p $UPLOAD_DIRECTORY