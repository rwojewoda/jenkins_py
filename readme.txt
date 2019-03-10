sudo supervisorctl status
sudo supervisorctl stop flask_app
sudo supervisorctl start flask_app

https://docs.dataplicity.com/docs/control-gpios-using-rest-api

export FLASK_APP=controller2.py

sudo -E flask run --host=0.0.0.0 --port=80

docker run --device /dev/mem:/dev/mem --device /dev/ttyAMA0:/dev/ttyAMA0 --privileged -ti YOUR_IMAGE_HERE /bin/bash