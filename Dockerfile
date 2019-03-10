FROM acencini/rpi-python-serial-wiringpi
MKDIR app
COPY app/* app
EXPOSE 80