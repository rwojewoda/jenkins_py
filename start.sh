#!/usr/bin/env bash

chown -R mpd:mpd /mnt/music

mkdir -p /mnt/music/playlists
chmod -R 777 /mnt/music/playlists

mkdir -p /mnt/music/.mpd
chmod -R 777 /mnt/music/.mpd

touch /mnt/music/.mpd/tag_cache
touch /mnt/music/.mpd/state

ls -al /mnt/music

mpd --no-daemon --stdout -v /etc/mpd.conf