from nanpy import DallasTemperature

#arduino = Arduino()
#a.pinMode(13, a.OUTPUT)
#a.digitalWrite(13, a.HIGH)
# o = OneWire(a)

sensors = DallasTemperature(2)


addr = sensors.getAddress(2)
sensors.requestTemperatures()


temp = sensors.getTempC(addr)

print temp

