#!/bin/sh

docker pull davout123/py
docker container rm -f dckr
docker run -p 6601:6600 -p 8001:8000 --name dckr --device=/dev/snd:/dev/snd -d davout123/py