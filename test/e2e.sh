#!/usr/bin/env bash

BASE_URL="http://0.0.0.0:8000"
BASE_KEY="xxx/yyy"

curl -H 'Accept: application/json' -F 'file=@./dante.txt;type=text/plain' "$BASE_URL/$BASE_KEY/dante.txt"
echo
curl -H 'Accept: application/json' -F 'file=@./dante.txt;type=text/plain' "$BASE_URL/$BASE_KEY/test.http"
echo
curl -H 'Accept: application/json' -F 'file=@./dante.txt;type=text/plain' "$BASE_URL/$BASE_KEY/zzz/dante.txt"
echo
curl "$BASE_URL/$BASE_KEY/dante.txt"
echo
curl "$BASE_URL/$BASE_KEY/"
echo
curl --request DELETE "$BASE_URL/$BASE_KEY/dante.txt"
echo
curl --request DELETE "$BASE_URL/$BASE_KEY/test.http"
echo
curl --request DELETE "$BASE_URL/$BASE_KEY/zzz/dante.txt"
echo
