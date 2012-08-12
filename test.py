import serial

USB_PORT = "/dev/ttyUSB0"

arduino = serial.Serial(USB_PORT, 9600)
print arduino.readline()
arduino.close()