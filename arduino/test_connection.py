import serial

locations = [
    'COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10',
    '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5',
    '/dev/ttyUSB6', '/dev/ttyUSB7', '/dev/ttyUSB8', '/dev/ttyUSB9',
    '/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', '/dev/ttyS5',
    '/dev/ttyS6', '/dev/ttyS7', '/dev/ttyS8', '/dev/ttyS9',
    ]

for device in locations:
    try:
        arduino = serial.Serial(device, 9600)
        print "Arduino 'might' be on", device
    except:
        pass

