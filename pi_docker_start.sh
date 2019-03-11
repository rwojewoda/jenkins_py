#!/bin/sh

docker pull davout123/py
docker container rm -f dckr
docker run -p 6601:6600 --user root --device /dev/snd --name dckr -d davout123/py