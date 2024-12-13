#!/bin/bash

USER_ID=$(id -u)
GROUP_ID=$(id -g)

echo "Environment Variables: $TEST, $PATH"
echo "User ID: $USER_ID, Group ID: $GROUP_ID"

exec "$@"
