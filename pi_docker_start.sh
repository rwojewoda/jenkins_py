#!/bin/sh

docker pull davout123/py
docker container rm -f dckr
docker run -p 6601:6601 -p 8001:8001 --name dckr --device=/dev/snd:/dev/snd -d davout123/py