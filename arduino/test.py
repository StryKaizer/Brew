import serial

port = 'COM4'

arduino = serial.Serial(port, 9600)


while 1:
# arduino.write("H")  # 72
    arduino.write('{"heat": 1, "stir": 1}')
    print arduino.readline()
    print arduino.readline()
    print arduino.readline()
    print arduino.readline()
    arduino.write('{"heat": 0, "stir": 1}')
    print arduino.readline()
    print arduino.readline()
    print arduino.readline()
    print arduino.readline()
    print arduino.readline()
