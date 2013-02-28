from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from brew.tasks import init_mashing
from brew.helpers import set_variable
from brew.models import Batch, MashingTempLog
from django.utils.dateformat import format


@dajaxice_register
def start_mashing(request, batch_id):

    set_variable('mashing_active', 'TRUE')
    batch = Batch.objects.get(id=batch_id)
    init_mashing.delay(batch)
    return simplejson.dumps({'status': 200})


@dajaxice_register
def stop_mashing(request):
    set_variable('mashing_active', 'FALSE')
    return simplejson.dumps({'status': 200})

@dajaxice_register
def chart_update(request, batch_id, greaterthan_templog_id=None):

    if greaterthan_templog_id:
        logs = MashingTempLog.objects.filter(batch__id=batch_id, id__gt=greaterthan_templog_id)
    else:
        logs = MashingTempLog.objects.filter(batch__id=batch_id)

    if len(logs) > 0:
        latest_templog_id = logs.latest('id').id
    else:
        latest_templog_id = None



    data = {'chart': style_chart_data(logs), 'latest_templog_id': latest_templog_id}
    return simplejson.dumps({'status': 200, 'data': data})


def style_chart_data(mashing_temp_logs):
    result = []
    for mashing_temp_log in mashing_temp_logs:
        log = [mashing_temp_log.get_seconds_offset(), mashing_temp_log.degrees]
        result.append(log)
    return result


@dajaxice_register
def delete_mashing_data(request, batch_id):

    MashingTempLog.objects.filter(batch__id=batch_id).delete()
    return simplejson.dumps({'status': 200})