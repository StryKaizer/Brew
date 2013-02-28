# Demo script for raspberry pi communicating with an arduino.
# Note: make sure your pi firmware is up to date (https://github.com/Hexxeh/rpi-update)

from serial import Serial as s
arduino = s('/dev/ttyACM0', 9600)
arduino.readline()
while 1:
    arduino.write('{"heat": 0, "stir": 1}')
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.write('{"heat": 1, "stir": 1}')
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
    arduino.readline()
