#!/usr/bin/python

from flask import request
from flask_api import FlaskAPI
from sultan.api import Sultan
from flask import jsonify
import RPi.GPIO as GPIO
import re
import logging



app = FlaskAPI(__name__)
sultan = Sultan()

LEDS = {"green": 12, "red": 12}
PINS_USED ={11,12,29,31,33,35,37,36}
GPIO.setmode(GPIO.BOARD)
for pin in PINS_USED:
    GPIO.setup(pin, GPIO.OUT)
    
@app.route('/', methods=["GET"])
def testsad():
    return {
           "nic": "nic"
    			 }

@app.route('/status', methods=["GET"])
def rasp_status():
    return {
           "hifi_status": hifiStatus(),
           "volume": getVolume(),
           "bath_speaker_status": speakerStatus(),
           "currentSong": getCurrentSongDesc()
    			 }
				 
@app.route('/mpc/status', methods=["GET"])
def mpcStatus():
    mpcStatus = sultan.sudo("mpc status").run().stdout
    if len(mpcStatus) > 1:
        result = mpcStatus[1]
        app.logger.info(("Result mpc status: %s",result))
        if "play" in result:
            return "1"
        else:
            return "0"
    else:
        return "0"
        
@app.route('/mpc/switch', methods=["GET"])
def switchMpc():
    if mpcStatus() == "1":
        sultan.sudo("mpc stop").run()
    else:
        sultan.sudo("mpc play").run()
    return rasp_status()
  
@app.route('/mpc/play', methods=["GET"])
def playMpc():
    sultan.sudo("mpc play").run()
    return "Mpc set to play"
    
@app.route('/mpc/song/number', methods=["GET"])
def getCurrentSongNumber():
    mpcStatus = sultan.sudo("mpc status").run().stdout
    if len(mpcStatus) > 1:
        result = mpcStatus[1]
        return result[11:12]
    else:
        return ""
 
@app.route('/mpc/song', methods=["GET"])
def getCurrentSongDesc():
    mpcStatus = sultan.sudo("mpc status").run().stdout
    if len(mpcStatus) == 1:
        return "Nic nie gra aktualnie"
    else:
        return mpcStatus[0]
        
@app.route('/mpc/song/<int:param>', methods=["GET"])
def getSongDesc(param):
    mpcStatus = sultan.sudo("mpc playlist").run().stdout
    if len(mpcStatus) > param:
        return mpcStatus[param]
    else:
        return ""
        
@app.route('/mpc/play/<int:param>', methods=["GET"])
def playSong(param):
    mpcStatus = sultan.sudo("mpc play " + str(param)).run().stdout
    return "Played " + str(param)

@app.route('/music/play', methods=["GET"])
def hifiStart():
    sultan.sudo("./scripts/switch_hifi").run()
    return rasp_status();
    
@app.route('/music', methods=["GET"])
def hifiStatus():
    return sultan.sudo("./scripts/hifi_status").run().stdout[0]
    
@app.route('/blinds/livingroom/down', methods=["GET"])
def salonScrAllDown():
    sultan.sudo("./scripts/r.sal.alldown").run()
    return "Living room blinders goes down"

@app.route('/blinds/livingroom/up', methods=["GET"])
def salonScrAllUp():
    sultan.sudo("./scripts/r.sal.allup").run()
    return "Living room blinders goes up"

@app.route('/blinds/bedroom/up', methods=["GET"])
def bedroomScrAllUp():
    sultan.sudo("./scripts/r.sypd.allup").run()
    return "Living room blinders goes up"

@app.route('/blinds/bedroom/down', methods=["GET"])
def bedroomScrAllDown():
    sultan.sudo("./scripts/r.sypd.alldown").run()
    return "Living room blinders goes up"
    
@app.route('/blinds/livingroom/go_up', methods=["GET"])
def salonScrUp():
    GPIO.output(29,1)
    return "Living room blinders goes up"

@app.route('/blinds/livingroom/go_up_stop', methods=["GET"])
def salonScrUpStop():
    GPIO.output(29,0)
    return "Living room blinders goes up"

@app.route('/blinds/livingroom/go_down', methods=["GET"])
def salonScrDown():
    GPIO.output(31,1)
    return "Living room blinders goes up"

@app.route('/blinds/livingroom/go_down_stop', methods=["GET"])
def salonScrDownStop():
    GPIO.output(31,0)
    return "Living room blinders goes up"

@app.route('/blinds/allup', methods=["GET"])
def blindsAllUp():
    sultan.sudo("./scripts/r.allup").run()
    return "All blinds going up"


@app.route('/blinds/alldown', methods=["GET"])
def blindsAllDown():
    sultan.sudo("./scripts/r.alldown").run()
    return "All blinds going down"

    
@app.route('/speaker/switch', methods=["GET"])
def speakerSwitch():
    if GPIO.input(12)==0:
         GPIO.output(12,1)
    else:
         GPIO.output(12,0)
    return speakerStatus()
 
@app.route('/speaker', methods=["GET"])
def speakerStatus():
    return str(GPIO.input(12))
    
@app.route('/sound/volume', methods=["GET"])
def getVolume():
    if mpcStatus()=="0":
        return "0"
    else:
        volume = sultan.sudo("amixer sget Headphone | grep 'Right:' | awk -F'[][]' '{ print $2 }'").run().stdout
        return volume[0][:-1]
    
@app.route('/sound/volume/up', methods=["GET"])
def setVolumeUp():
    volume = int(getVolume()) +10
    app.logger.info(("volume",volume))
    sultan.sudo("amixer --quiet set Headphone " + str(volume) + "%").run()
    return getVolume()
    
@app.route('/sound/volume/down', methods=["GET"])
def setVolumeDown():
    volume = int(getVolume()) - 10
    app.logger.info(("volume",volume))
    sultan.sudo("amixer --quiet set Headphone " +  str(volume) + "%").run()
    return getVolume()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(threaded=True)