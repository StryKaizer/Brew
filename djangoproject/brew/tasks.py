from celery import task
from brew.models import MashLog, Batch
from brew.helpers import get_variable, set_variable
from time import sleep
from random import random
from datetime import datetime
from django.conf import settings
import pytz

MASHSTEP_STATE_APPROACH = 'approach'
MASHSTEP_STATE_STAY = 'stay'
MASHSTEP_STATE_FINISHED = 'finished'
ARDUINO_TEMPERATURE_PIN = 2
MAXIMUM_DEVIATION = 0.3  # Maximum allowed deviation in temperature before heat/cooling is triggered
DELAY_BETWEEN_MEASUREMENTS = 2  # Seconds between each measurement
DELAY_BETWEEN_ACTION_SWITCH = 30  # To prevent fast switching between heat, passive and/or cooling, add build in delay

@task()
def init_mashing(batch):
    # Set defaults for batch on start
    batch.active_mashingstep = batch.mashing_scheme.mashingstep_set.all().order_by('position')[0]
    batch.active_mashingstep_state = MASHSTEP_STATE_APPROACH
    batch.active_mashingstep_state_start = datetime.now(pytz.utc)
    batch.active_mashingstep_approach_direction = 'tbd'
    batch.heat = False
    batch.cool = False
    batch.save()

    # Initialize Arduino with Nanpy
    if not settings.ARDUINO_SIMULATION:
        from nanpy import DallasTemperature # Nanpy Initializes Arduino connection, thus using conditional import
        sensor = DallasTemperature(ARDUINO_TEMPERATURE_PIN)
        addr = sensor.getAddress(ARDUINO_TEMPERATURE_PIN)

    # Run Mashing proces
    while batch.mashing_process_is_running:
        sleep(DELAY_BETWEEN_MEASUREMENTS)
        print 'running'

        # Measure data
        measured_data = {}
        if settings.ARDUINO_SIMULATION:
            measured_data['temp'] = get_dummy_temperature(batch)
        else:
            sensor.requestTemperatures()
            measured_data['temp'] = sensor.getTempC(addr)

        # Define actions depending on measured data
        batch = process_measured_data(batch.id, measured_data)

        # Optionally, Log everything
        MashLog.objects.create(
            batch=batch,
            degrees=measured_data['temp'],
            active_mashing_step=batch.active_mashingstep,
            active_mashing_step_state=batch.active_mashingstep_state,
            heat=batch.heat,
            chart_icon=None
        )

    return 'Mashing proces ended'


# Update batch data according to measured data
def process_measured_data(batch_id, measured_data):
    # Ensure up to date batch
    batch = Batch.objects.get(id=batch_id)

    temp = float(measured_data['temp'])

    # current mashing action is heat/cool until next step is reached
    if batch.active_mashingstep_state == MASHSTEP_STATE_APPROACH:
        switch_to_stay = False

        # Cast to float
        target_temperature = float(batch.active_mashingstep.degrees)

        # Define direction if undefined and start appropriate action
        if batch.active_mashingstep_approach_direction == 'tbd':
            if temp < target_temperature:
               batch.active_mashingstep_approach_direction = 'heat' 
               batch.heat = True
            else:
                batch.active_mashingstep_approach_direction = 'cool'
                batch.cool = True

        # Healing logic
        if batch.active_mashingstep_approach_direction == 'heat' and temp >= target_temperature:
            # Mashing step temperature reached
            switch_to_stay = True

        # Cooling logic
        if batch.active_mashingstep_approach_direction == 'cool'and temp <= target_temperature:
            # Mashing step temperature reached
            switch_to_stay = True

        # Mashing step degrees reached logic
        if switch_to_stay:
            # Switch to stay at temperature
            batch.active_mashingstep_state = MASHSTEP_STATE_STAY
            batch.heat = False
            batch.cool = False
            # Reset direction
            batch.active_mashingstep_approach_direction = 'tbd'


    elif batch.active_mashingstep_state == MASHSTEP_STATE_STAY:

        # Check if total time to spend in active mashing step is reached
        seconds_to_stay = int(batch.active_mashingstep.minutes) * 60
        now = datetime.now(pytz.utc)
        difference = now - batch.active_mashingstep_state_start
        if difference.total_seconds() >= seconds_to_stay:
            # Total time to spend in active mashing step reached
            # If active mashing step is latest, set status to finished
            active_mashing_step_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=batch.active_mashingstep.id).count()
            try:
                # Activate next mashing step if available
                batch.active_mashingstep = batch.mashing_scheme.mashingstep_set.all()[active_mashing_step_index + 1]
                batch.active_mashingstep_state = MASHSTEP_STATE_APPROACH
            except:
                # Set state to finished
                batch.active_mashingstep_state = MASHSTEP_STATE_FINISHED

        else:
            # Total time spend not reached, check if actions are required to ensure current temperature
            target_temperature = float(batch.active_mashingstep.degrees)

            # TODO: Set actions if temperature goes out of bounds
            # if temp < (temp_to_stay - MAXIMUM_DEVIATION) and
    batch.save()
    return batch


# Return dummy temp for testing based on heat/cool actions triggered
def get_dummy_temperature(batch):
    try:
        # Generate semi random temperature based on previous fake temp
        previous_mash_log = MashLog.objects.filter(batch=batch).latest('id')

        if previous_mash_log.heat:
            # When previous log was heating, simulate steady temperature raising
            temp = "%.2f" % (previous_mash_log.degrees + (random() / 10))
        else:
            # Nothing happening, simulate slow temperature lowering
            temp = "%.2f" % (previous_mash_log.degrees - (random() / 150))

    except MashLog.DoesNotExist:
        # Start dummy temp
        temp = 20
    return temp