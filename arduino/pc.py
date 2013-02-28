# Demo script for raspberry pi communicating with an arduino.
# Note: make sure your pi firmware is up to date (https://github.com/Hexxeh/rpi-update)

import serial
import time

port = 'COM4'
baud = 9600


while True:
    try:
        arduino = serial.Serial(port, baud)
        break
    except:
        print 'waiting for device ' + port + ' to be available'
        time.sleep(3)

for x in range(0, 5):

    arduino.write('{"heat": 0, "stir": 1}')
    data = arduino.readline().strip('\r\n')
    print data
    data = arduino.readline().strip('\r\n')
    print data
    data = arduino.readline().strip('\r\n')
    print data

    data = arduino.readline().strip('\r\n')
    print data
    data = arduino.readline().strip('\r\n')
    print data
    data = arduino.readline().strip('\r\n')
    print data
    arduino.write('{"heat": 1, "stir": 1}')
    data = arduino.readline().strip('\r\n')
    print data
    data = arduino.readline().strip('\r\n')
    print data

arduino.close()