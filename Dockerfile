FROM acencini/rpi-python-serial-wiringpi
RUN mkdir /app
COPY app/* app
EXPOSE 80