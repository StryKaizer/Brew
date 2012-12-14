from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from brew.tasks import init_mashing
from brew.helpers import set_variable
from brew.models import BrewingDay, MashingTempLog

from django.utils.dateformat import format


@dajaxice_register
def start_mashing(request):

    set_variable('mashing_active', 'TRUE')
    brewing_day = BrewingDay.objects.latest('id')
    init_mashing.delay(brewing_day)
    return simplejson.dumps({'status':200})


@dajaxice_register
def stop_mashing(request):
    set_variable('mashing_active', 'FALSE')
    return simplejson.dumps({'status':200})

@dajaxice_register
def chart_update_all(request):
    brewing_day_id = 1
    data = {}
    brewing_day = BrewingDay.objects.get(id=brewing_day_id)
    logs = MashingTempLog.objects.filter(brewing_day=brewing_day)
    data['chart'] = style_chart_data(logs)
    return simplejson.dumps({'status':200, 'data': data})

@dajaxice_register
def chart_update_latest(request):
    brewing_day_id = 1
    data = {}
    data['chart'] = style_chart_data([MashingTempLog.objects.latest('id')])
    return simplejson.dumps({'status':200, 'data': data})





def style_chart_data(mashing_temp_logs):
    result = []
    for mashing_temp_log in mashing_temp_logs:
        # log = [mashing_temp_log.created.isoformat(), mashing_temp_log.degrees]
        log = [mashing_temp_log.get_seconds_offset(), mashing_temp_log.degrees]
        result.append(log)
    return result
