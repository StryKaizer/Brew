from celery import task
from brew.models import MashLog, Batch
from brew.helpers import get_variable, set_variable
from time import sleep
from random import random
from datetime import datetime
from django.conf import settings
from nanpy import DallasTemperature, Arduino
import pytz

MASHSTEP_STATE_APPROACH = 'approach'
MASHSTEP_STATE_STAY = 'stay'
MASHSTEP_STATE_FINISHED = 'finished'
ARDUINO_TEMPERATURE_PIN = 2
ARDUINO_HEAT_PIN = 11
ARDUINO_COOL_PIN = 12
ARDUINO_STATUS_PIN = 13
MAXIMUM_DEVIATION = 0.3  # Maximum allowed deviation in temperature before heat/cooling is triggered
DELAY_BETWEEN_MEASUREMENTS = 2  # Seconds between each measurement
DELAY_BETWEEN_LOGS = 15  # Seconds between each measurement
DELAY_BETWEEN_ACTION_SWITCH = 30  # To prevent fast switching between heat, passive and/or cooling, add build in delay

@task()
def init_mashing(batch):

    # (Re)set defaults for batch
    set_batch_defaults(batch)
    set_variable('active_mashingprocess_batch_id', str(batch.id))

    # Initialize Arduino with Nanpy
    if not settings.ARDUINO_SIMULATION:
        sensor = DallasTemperature(ARDUINO_TEMPERATURE_PIN)
        addr = sensor.getAddress(ARDUINO_TEMPERATURE_PIN)
        Arduino.pinMode(ARDUINO_HEAT_PIN, Arduino.OUTPUT)
        Arduino.pinMode(ARDUINO_COOL_PIN, Arduino.OUTPUT)
        Arduino.pinMode(ARDUINO_STATUS_PIN, Arduino.OUTPUT)
        Arduino.digitalWrite(ARDUINO_HEAT_PIN, Arduino.LOW)
        Arduino.digitalWrite(ARDUINO_COOL_PIN, Arduino.LOW)
        Arduino.digitalWrite(ARDUINO_STATUS_PIN, Arduino.HIGH)
    else:
        # Set initial dummy temperature
        batch.temperature = 20  # Testing purpose only
        batch.save()
        batch = Batch.objects.get(id=batch.id)

    # Run Mashing proces
    while get_variable('active_mashingprocess_batch_id', 'None') == str(batch.id):
        # Measure data
        measured_data = {}
        if settings.ARDUINO_SIMULATION:
            measured_data['temp'] = get_dummy_temperature(batch)
        else:
            sensor.requestTemperatures()
            measured_data['temp'] = sensor.getTempC(addr)

        # Define actions depending on measured data
        batch = process_measured_data(batch.id, measured_data)

        # Send updates to arduino
        if not settings.ARDUINO_SIMULATION:
            send_updates_to_arduino(batch)

        # Send to logging department
        handle_logging(batch)

        # Delay
        sleep(DELAY_BETWEEN_MEASUREMENTS)

    Arduino.digitalWrite(ARDUINO_STATUS_PIN, Arduino.LOW)
    Arduino.digitalWrite(ARDUINO_COOL_PIN, Arduino.LOW)
    Arduino.digitalWrite(ARDUINO_HEAT_PIN, Arduino.LOW)

    return 'Mashing proces ended'


# Update batch data according to measured data
def process_measured_data(batch_id, measured_data):
    # Ensure up to date batch
    batch = Batch.objects.get(id=batch_id)
    batch.temperature = float(measured_data['temp'])
    temp = float(measured_data['temp'])

    # current mashing action is heat/cool until next step is reached
    if batch.active_mashingstep_state == MASHSTEP_STATE_APPROACH:
        switch_to_stay = False

        # Cast to float
        target_temperature = float(batch.active_mashingstep.temperature)

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

        # Mashing step temperature reached logic
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
            active_mashingstep_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=batch.active_mashingstep.id).count()
            try:
                # Activate next mashing step if available
                batch.active_mashingstep = batch.mashing_scheme.mashingstep_set.all()[active_mashingstep_index + 1]
                batch.active_mashingstep_state = MASHSTEP_STATE_APPROACH
            except:
                # Set state to finished
                batch.active_mashingstep_state = MASHSTEP_STATE_FINISHED

        else:
            # Total time spend not reached, check if actions are required to ensure current temperature
            target_temperature = float(batch.active_mashingstep.temperature)

            # TODO: Set actions if temperature goes out of bounds
            # if temp < (temp_to_stay - MAXIMUM_DEVIATION) and
    batch.save()
    return batch

def handle_logging(batch):
    chart_icon = None
    create_log = False

    try:
        last_log = MashLog.objects.filter(batch=batch).latest('id')
        now = datetime.now(pytz.utc)
        difference = now - last_log.created

        #  If DELAY_BETWEEN_LOGS is reached, log!
        if difference.total_seconds() >= DELAY_BETWEEN_LOGS:
            create_log = True

        # If state changed since previous log, log!
        if last_log.active_mashing_step_state != batch.active_mashingstep_state:
            create_log = True

            # Set chart icon
            if batch.active_mashingstep_state == MASHSTEP_STATE_STAY:
                active_mashingstep_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=batch.active_mashingstep.id).count()
                chart_icon = 'start' + str(active_mashingstep_index + 1)
            elif batch.active_mashingstep_state == MASHSTEP_STATE_APPROACH:
                active_mashingstep_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=batch.active_mashingstep.id).count()
                chart_icon = 'stop' + str(active_mashingstep_index)
            elif batch.active_mashingstep_state == MASHSTEP_STATE_FINISHED:
                chart_icon = 'finished'

    except MashLog.DoesNotExist:
        #  No logs found, log first one
        create_log = True

    if create_log:
        # Optionally, Log everything
        MashLog.objects.create(
            batch=batch,
            temperature=batch.temperature,
            active_mashing_step=batch.active_mashingstep,
            active_mashing_step_state=batch.active_mashingstep_state,
            heat=batch.heat,
            chart_icon=chart_icon
        )


# (Re)Set initial status for batch
def set_batch_defaults(batch):
    batch.active_mashingstep = batch.mashing_scheme.mashingstep_set.all().order_by('position')[0]
    batch.active_mashingstep_state = MASHSTEP_STATE_APPROACH
    batch.active_mashingstep_state_start = datetime.now(pytz.utc)
    batch.active_mashingstep_approach_direction = 'tbd'
    batch.heat = False
    batch.cool = False
    batch.save()


def send_updates_to_arduino(batch):
    if batch.heat:
        Arduino.digitalWrite(ARDUINO_HEAT_PIN, Arduino.HIGH)
    else:
        Arduino.digitalWrite(ARDUINO_HEAT_PIN, Arduino.LOW)

    if batch.cool:
        Arduino.digitalWrite(ARDUINO_COOL_PIN, Arduino.HIGH)
    else:
        Arduino.digitalWrite(ARDUINO_COOL_PIN, Arduino.LOW)


# Return dummy temp for testing based on heat/cool actions triggered
def get_dummy_temperature(batch):
    if batch.heat:
        # When heating, simulate steady temperature raising
        temp = "%.2f" % (batch.temperature + (random() / 10))
    else:
        # Nothing happening, simulate slow temperature lowering
        temp = "%.2f" % (batch.temperature - (random() / 150))
    return temp