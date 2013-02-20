import serial

port = 'COM4'

arduino = serial.Serial(port, 9600)


while 1:
    # arduino.write("H")  # 72
    print arduino.readline()
    arduino.write("{'heat': 1}")