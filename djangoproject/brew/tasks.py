from celery import task
from brew.models import MashingTempLog
from brew.helpers import get_variable
from time import sleep

from random import randint

@task()
def init_mashing(batch):
    while get_variable('mashing_active', 'FALSE') == 'TRUE':

        sleep(2)  # Log om de 2 seconden
        temp = float(get_variable('dummytemp', 20.18))
        MashingTempLog.objects.create(batch=batch, degrees=temp)



    return 'Mashing proces ended'
