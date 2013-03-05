from celery import task
from brew.models import MashingTempLog
from brew.helpers import get_variable, set_variable
from time import sleep
from nanpy import DallasTemperature
from random import random
from django.conf import settings

@task()
def init_mashing(batch):
    set_variable('current_mashing_action', 'go_to_mashingstep')
    set_variable('go_to_mashingstep_direction', 'tbd')

    # Start up arduino connection
    if not settings.ARDUINO_SIMULATION:
        sensor = DallasTemperature(2)
        addr = sensor.getAddress(2)

    while get_variable('mashing_active', 'FALSE') == 'TRUE':
        sleep(2)  # Log om de 2 seconden

        if settings.ARDUINO_SIMULATION:
            try:
                # Generate semi random temperature based on previous fake temp
                previous = MashingTempLog.objects.filter(batch=batch).latest('id')
                temp = "%.2f" % ((random() / 10) + previous.degrees)
            except MashingTempLog.DoesNotExist:
                # Start dummy temp
                temp = 20
        else:
            # Get data from Arduino
            sensor.requestTemperatures()
            temp = sensor.getTempC(addr)

        result = get_mashing_actions(batch, temp)
        print result #TODO: actually use this ;)

        MashingTempLog.objects.create(batch=batch, degrees=temp)

    set_variable('mashing_batch_id_active', "0")
    return 'Mashing proces ended'


# Returns a dictionary with actions and a boolean for each action whether they need to be active
def get_mashing_actions(batch, temp):

    temp = float(temp)

    # current mashing action is heat/cool until next step is reached
    if get_variable('current_mashing_action') == 'go_to_mashingstep':
        switch_to_stay = False

        # Load step which we are trying to reach
        mashingschemeitems_finished = MashingTempLog.objects.filter(batch=batch).exclude(mashingschemeitem_started=None).count()
        mashingschemeitem = batch.mashing_scheme.mashingschemeitem_set.all()[mashingschemeitems_finished]

        # Cast to float
        temp_to_reach = float(mashingschemeitem.degrees)

        # If direction is unknown (cool or heat), define direction (First time in each go_to_mashingstep phase)
        if get_variable('go_to_mashingstep_direction') == 'tbd':
            if temp < temp_to_reach:
                set_variable('go_to_mashingstep_direction', 'heat')
            else:
                set_variable('go_to_mashingstep_direction', 'cool')

        # Healing logic
        if get_variable('go_to_mashingstep_direction') == 'heat':
            # Check if temperature is reached
            if temp >= temp_to_reach:
                # Mashingschemeitem temperature reached
                switch_to_stay = True
            else:
                return {'heat': True, 'cool': False}

        # Cooling logic
        if get_variable('go_to_mashingstep_direction') == 'cool':
            # Check if temperature is reached
            if temp <= temp_to_reach:
                # Mashingschemeitem temperature reached
                switch_to_stay = True
            else:
                return {'heat': False, 'cool': True}

        # mashingschemeitem degrees reached logic
        if switch_to_stay:
            # Switch to stay at temperature
            set_variable('current_mashing_action', 'stay_at_mashingstep')
            # Reset direction
            set_variable('go_to_mashingstep_direction', 'tbd')
            # set heat and cooling to false, and notify mashingschemeitem start
            return {'heat': False, 'cool': False, 'mashingschemeitem_started': mashingschemeitem}

    return False