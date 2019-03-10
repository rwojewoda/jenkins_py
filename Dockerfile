FROM balenalib/raspberry-pi2-alpine-python:3-edge-build

RUN echo "ipv6" >> /etc/modules
RUN apk update
RUN apk add alsa-utils
RUN apk add mpd

RUN groupadd mpd

ADD mpd.conf /etc/mpd.conf
ADD start.sh /home/mpd/start.sh

RUN mkdir -p /home/mpd/pids
RUN mkdir -p /home/mpd/logs

RUN chown -R mpd /home/mpd
RUN chmod +x /home/mpd/start.sh

EXPOSE 6600 8000

ENTRYPOINT /home/mpd/start.sh