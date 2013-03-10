from celery import task
from brew.models import MashLog
from brew.helpers import get_variable, set_variable
from time import sleep
from random import random
from django.conf import settings

MASHSTEP_STATE_HEAT = 'H'
MASHSTEP_STATE_COOL = 'C'
MASHSTEP_STATE_STAY = 'S'
MASHSTEP_STATE_FINISHED = 'F'
ARDUINO_TEMPERATURE_PIN = 2

@task()
def init_mashing(batch):
    set_variable('current_mashing_action', 'go_to_mashingstep')
    set_variable('go_to_mashingstep_direction', 'tbd')

    # Initialize Arduino with Nanpy
    if not settings.ARDUINO_SIMULATION:
        from nanpy import DallasTemperature # Nanpy Initializes Arduino connection, thus using conditional import
        sensor = DallasTemperature(ARDUINO_TEMPERATURE_PIN)
        addr = sensor.getAddress(ARDUINO_TEMPERATURE_PIN)

    # Run Mashing proces
    while get_variable('mashing_active', 'FALSE') == 'TRUE':
        sleep(2)  # Log om de 2 seconden

        # Measure data
        measured_data = {}
        if settings.ARDUINO_SIMULATION:
            measured_data['temp'] = get_dummy_temperature(batch)
        else:
            # Get data from Arduino
            sensor.requestTemperatures()
            measured_data['temp'] = sensor.getTempC(addr)

        # Define actions depending on measured data
        actions = get_mashing_actions(batch, measured_data)

        # Log everything
        MashLog.objects.create(
            batch=batch,
            degrees=temp,
            active_mashing_step=actions['active_mashing_step'],
            active_mashing_step_state=actions['state']
        )

    # End Mashing proces
    set_variable('mashing_batch_id_active', "0")
    return 'Mashing proces ended'


# Returns a dictionary with actions and a boolean for each action whether they need to be active
def get_mashing_actions(batch, measured_data):

    temp = float(measured_data['temp'])
    active_mashing_step = None

    # current mashing action is heat/cool until next step is reached
    if get_variable('current_mashing_action') == 'go_to_mashingstep':
        switch_to_stay = False

        # Load active mashing step
        try:
            # Try to get active mashing step from latest log
            active_mashing_step = MashLog.objects.filter(batch=batch).latest('id').active_mashing_step
        except MashLog.DoesNotExist:
            active_mashing_step = batch.mashing_scheme.mashingstep_set.all()[0]

        # Cast to float
        temp_to_reach = float(active_mashing_step.degrees)

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
                # Mashing step temperature reached
                switch_to_stay = True
            else:
                state = MASHSTEP_STATE_HEAT

        # Cooling logic
        if get_variable('go_to_mashingstep_direction') == 'cool':
            # Check if temperature is reached
            if temp <= temp_to_reach:
                # Mashing step temperature reached
                switch_to_stay = True
            else:
                state = MASHSTEP_STATE_COOL

        # Mashing step degrees reached logic
        if switch_to_stay:
            # Switch to stay at temperature
            set_variable('current_mashing_action', 'stay_at_mashingstep')
            # Reset direction
            set_variable('go_to_mashingstep_direction', 'tbd')
            # Change status
            state = MASHSTEP_STATE_STAY

    return {'state': state, 'active_mashing_step': active_mashing_step}


# Return dummy temp for testing
def get_dummy_temperature(batch):
    try:
        # Generate semi random temperature based on previous fake temp
        previous = MashLog.objects.filter(batch=batch).latest('id')
        temp = "%.2f" % ((random() / 10) + previous.degrees)
    except MashLog.DoesNotExist:
        # Start dummy temp
        temp = 20
    return temp