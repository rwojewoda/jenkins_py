FROM balenalib/raspberry-pi2-alpine-python:3-edge-build

ENV MPD_VERSION 0.19.12-r0
ENV MPC_VERSION 0.27-r0

# https://docs.docker.com/engine/reference/builder/#arg
ARG user=mpd
ARG group=audio

RUN apk -q update
RUN apk -q --no-progress add mpd
RUN apk -q --no-progress add mpc
RUN rm -rf /var/cache/apk/*

RUN mkdir -p /var/lib/mpd/music \
    && mkdir -p /var/lib/mpd/playlists \
    && mkdir -p /var/lib/mpd/database \
    &&  echo "" > /var/log/mpd/mpd.log \
    && chown -R ${user}:${group} /var/lib/mpd \
    && chown -R ${user}:${group} /var/log/mpd/mpd.log

RUN mpc add http://ant-waw-02.cdn.eurozet.pl:8602/

# Declare a music , playlists and database volume (state, tag_cache and sticker.sql)
VOLUME ["/var/lib/mpd/music", "/var/lib/mpd/playlists", "/var/lib/mpd/database"]
COPY mpd.conf /etc/mpd.conf

# Entry point for mpc update and stuff
EXPOSE 6600
EXPOSE 8001
CMD ["mpd", "--stdout", "--no-daemon"]