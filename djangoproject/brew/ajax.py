from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from brew.tasks import init_mashing
from brew.helpers import set_variable
from brew.models import Batch, MashLog
from django.utils.dateformat import format


@dajaxice_register
def start_mashing(request, batch_id):
    set_variable('active_mashingprocess_batch_id', str(batch_id))
    batch = Batch.objects.get(id=batch_id)
    init_mashing.delay(batch)
    return simplejson.dumps({'status': 200})


@dajaxice_register
def stop_mashing(request, batch_id):
    set_variable('active_mashingprocess_batch_id', 'None')
    return simplejson.dumps({'status': 200})


@dajaxice_register
def chart_update(request, batch_id, greaterthan_mashlog_id=None):

    batch = Batch.objects.get(id=batch_id)

    if greaterthan_mashlog_id:
        mash_logs = MashLog.objects.filter(batch__id=batch_id, id__gt=greaterthan_mashlog_id)
    else:
        mash_logs = MashLog.objects.filter(batch__id=batch_id)

    if len(mash_logs) > 0:
        latest_mashlog_id = mash_logs.latest('id').id
    else:
        latest_mashlog_id = None

    active_mashingstep_index = batch.mashing_scheme.mashingstep_set.filter(id__lt=batch.active_mashingstep.id).count()


    data = {
        'chart': style_chart_data(mash_logs),
        'latest_mashlog_id': latest_mashlog_id,
        'active_mashingstep_index': active_mashingstep_index,
        'active_mashingstep_state': batch.active_mashingstep_state,
        # 'active_mashingstep_state_start': batch.active_mashingstep_state_start,
        'temperature': batch.temperature,
        'heat': batch.heat,
        'cool': batch.cool,
        
    }
    return simplejson.dumps({'status': 200, 'data': data})


def style_chart_data(mash_logs):
    result = []
    for mash_log in mash_logs:
        log = {
            'seconds': mash_log.get_seconds_offset(),
            'temperature': mash_log.temperature,
            'icon': mash_log.chart_icon,
        }
        result.append(log)
    return result


@dajaxice_register
def delete_mashing_data(request, batch_id):
    MashLog.objects.filter(batch__id=batch_id).delete()
    return simplejson.dumps({'status': 200})