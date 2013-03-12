from celery import task
from brew.models import MashLog
from brew.helpers import get_variable, set_variable
from time import sleep
from random import random
from datetime import datetime
from django.conf import settings
import pytz

MASHSTEP_STATE_APPROACH = 'A'
MASHSTEP_STATE_STAY = 'S'
MASHSTEP_STATE_FINISHED = 'F'
ARDUINO_TEMPERATURE_PIN = 2
MAXIMUM_DEVIATION = 0.3  # Maximum allowed deviation in temperature before heat/cooling is triggered
DELAY_BETWEEN_MEASUREMENTS = 2  # Seconds between each measurement
DELAY_BETWEEN_ACTION_SWITCH = 30  # To prevent fast switching between heat, passive and/or cooling, add build in delay

@task()
def init_mashing(batch):
    set_variable('current_mashing_action', 'approach_mashingstep') # TODO: remove this, is obsolete now as we keep state in logs
    set_variable('approach_mashingstep_direction', 'tbd')
    set_variable('mashing_batch_id_active', str(batch.id))

    # Initialize Arduino with Nanpy
    if not settings.ARDUINO_SIMULATION:
        from nanpy import DallasTemperature # Nanpy Initializes Arduino connection, thus using conditional import
        sensor = DallasTemperature(ARDUINO_TEMPERATURE_PIN)
        addr = sensor.getAddress(ARDUINO_TEMPERATURE_PIN)

    # Run Mashing proces
    while get_variable('mashing_active', 'FALSE') == 'TRUE':
        sleep(DELAY_BETWEEN_MEASUREMENTS)

        # Measure data
        measured_data = {}
        if settings.ARDUINO_SIMULATION:
            measured_data['temp'] = get_dummy_temperature(batch)
        else:
            sensor.requestTemperatures()
            measured_data['temp'] = sensor.getTempC(addr)

        # Define actions depending on measured data
        processed = process_measured_data(batch, measured_data)

        # Log everything
        MashLog.objects.create(
            batch=batch,
            degrees=measured_data['temp'],
            active_mashing_step=processed['active_mashing_step'],
            active_mashing_step_state=processed['state'],
            heat=processed['actions']['heat'],
            chart_icon=processed['chart_icon']
        )

    # End Mashing proces
    set_variable('mashing_batch_id_active', "0")
    return 'Mashing proces ended'


# Return actions, active step and state dependong on measured data
def process_measured_data(batch, measured_data):
    actions = {'heat': False, 'cool': False}
    active_mashing_step = None
    chart_icon = None
    state = None
    temp = float(measured_data['temp'])

    # current mashing action is heat/cool until next step is reached
    if get_variable('current_mashing_action') == 'approach_mashingstep':
        switch_to_stay = False

        # Load active mashing step
        try:
            active_mashing_step = MashLog.objects.filter(batch=batch).latest('id').active_mashing_step
        except MashLog.DoesNotExist:
            active_mashing_step = batch.mashing_scheme.mashingstep_set.all()[0]

        # Cast to float
        temp_to_reach = float(active_mashing_step.degrees)

        # If direction is unknown (cool or heat), define direction (First time in each approach mashingstep phase)
        if get_variable('approach_mashingstep_direction') == 'tbd':
            if temp < temp_to_reach:
                set_variable('approach_mashingstep_direction', 'heat')
            else:
                set_variable('approach_mashingstep_direction', 'cool')

        # Healing logic
        if get_variable('approach_mashingstep_direction') == 'heat':
            # Check if temperature is reached
            if temp >= temp_to_reach:
                # Mashing step temperature reached
                switch_to_stay = True
            else:
                state = MASHSTEP_STATE_APPROACH
                actions['heat'] = True

        # Cooling logic
        if get_variable('approach_mashingstep_direction') == 'cool':
            # Check if temperature is reached
            if temp <= temp_to_reach:
                # Mashing step temperature reached
                switch_to_stay = True
            else:
                state = MASHSTEP_STATE_APPROACH
                actions['cool'] = True

        # Mashing step degrees reached logic
        if switch_to_stay:
            # Switch to stay at temperature
            set_variable('current_mashing_action', 'stay_at_mashingstep')
            # Reset direction
            set_variable('approach_mashingstep_direction', 'tbd')
            # Change status
            state = MASHSTEP_STATE_STAY
            # Set chart icon in log
            active_mashing_step_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=active_mashing_step.id).count()
            chart_icon = 'start' + str((active_mashing_step_index + 1))

    elif get_variable('current_mashing_action') == 'stay_at_mashingstep':
        active_mashing_step = MashLog.objects.filter(batch=batch).latest('id').active_mashing_step

        # Check if total time to spend in active mashing step is reached
        seconds_to_stay = int(active_mashing_step.minutes) * 60
        first_log_for_current_mashing_step = MashLog.objects.filter(batch=batch, active_mashing_step=active_mashing_step, active_mashing_step_state='S')[0]
        now = datetime.now(pytz.utc)
        difference = now - first_log_for_current_mashing_step.created
        if difference.total_seconds() >= seconds_to_stay:
            # Total time to spend in active mashing step reached
            # If active mashing step is latest, set status to finished
            active_mashing_step_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=active_mashing_step.id).count()
            try:
                # Activate next mashing step if available
                active_mashing_step = batch.mashing_scheme.mashingstep_set.all()[active_mashing_step_index + 1]
                state = MASHSTEP_STATE_APPROACH
                set_variable('current_mashing_action', 'approach_mashingstep')
                chart_icon = 'stop' + str((active_mashing_step_index + 1))
            except:
                # Set state to finished
                state = MASHSTEP_STATE_FINISHED
                set_variable('current_mashing_action', 'finished')

        else:
            # Total time spend not reached, check if actions are required to ensure current temperature
            temp_to_stay = float(active_mashing_step.degrees)
            state = MASHSTEP_STATE_STAY

            # TODO: Set actions if temperature goes out of bounds
            # if temp < (temp_to_stay - MAXIMUM_DEVIATION) and
    elif get_variable('current_mashing_action') == 'finished':
        state = MASHSTEP_STATE_FINISHED
        active_mashing_step = MashLog.objects.filter(batch=batch).latest('id').active_mashing_step

    return {'state': state, 'active_mashing_step': active_mashing_step, 'actions': actions, 'chart_icon': chart_icon}


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