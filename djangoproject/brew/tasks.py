from celery import task
from brew.models import MashingTempLog
from brew.helpers import get_variable, set_variable
from time import sleep
from nanpy import DallasTemperature
from random import random
from django.conf import settings

@task()
def init_mashing(batch):


    set_variable('mashing_batch_id_active', str(batch.id))
    # Start up arduino connection
    if not settings.ARDUINO_SIMULATION:
        sensor = DallasTemperature(2)
        addr = sensor.getAddress(2)

    while get_variable('mashing_active', 'FALSE') == 'TRUE':
        sleep(2)  # Log om de 2 seconden

        if settings.ARDUINO_SIMULATION:
            try:
                # Generate semi random temperature based on previous fake temp
                previous = MashingTempLog.objects.latest('id')
                temp = (random() / 20) + previous.degrees
            except:
                # Start dummy temp
                temp = 20
        else:
            # Get data from Arduino
            sensor.requestTemperatures()
            temp = sensor.getTempC(addr)



        

        MashingTempLog.objects.create(batch=batch, degrees=temp)

    set_variable('mashing_batch_id_active', "0")
    return 'Mashing proces ended'
