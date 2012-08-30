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
def update(request):
    brewing_day_id = 1
    data = {}
    brewing_day = BrewingDay.objects.get(id=brewing_day_id)
    data['chart'] = get_chart_data(brewing_day)
    
    return simplejson.dumps({'status':200, 'data': data})






# TODO
def get_chart_data(brewing_day):
    #return ['jjj', 'fjoesqjf']
    result = []
    for mashing_temp_log in MashingTempLog.objects.filter(brewing_day=brewing_day):
        #timestamp
        #result.append({'Date.UTC(2012,  2, 11, 0,0,0)', 'ff'})
        b = {'ji': 'jojp'}
        #result.append(format(mashing_temp_log.created, 'U'))
        result.append(b)
    return result
