#!/bin/bash

#domain="https://qlsc2jgvt7.execute-api.us-east-1.amazonaws.com/staging"
domain="https://14tov54r77.execute-api.us-east-1.amazonaws.com/staging"
#domain="https://short.copc.io"

resp=$(curl  -s -H "Accept: application/json" -H "Content-type: application/json" -XPOST "$domain/" -d '{
	"state": "a bunch of junk"
}')


echo "received: $resp"
id=$(jq -r '.url' <<< $resp)
echo "id is: $id"

curl "$domain/$id"
