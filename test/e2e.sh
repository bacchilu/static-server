#!/usr/bin/env bash

curl -H 'Accept: application/json' -F 'file=@./dante.txt;type=text/plain' http://0.0.0.0:8000/xxx/yyy | jq
echo "------------------------------------------------------------"
curl http://0.0.0.0:8000/xxx/yyy/dante.txt | { cat; printf '\n'; }
echo "------------------------------------------------------------"
curl http://0.0.0.0:8000/xxx/yyy/ | jq
echo "------------------------------------------------------------"
curl --request DELETE http://0.0.0.0:8000/xxx/yyy/dante.txt | jq