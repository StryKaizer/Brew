from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from brew.tasks import init_mashing
from brew.helpers import set_variable
from brew.models import Batch, MashLog
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
def chart_update(request, batch_id, greaterthan_mashlog_id=None):

    if greaterthan_mashlog_id:
        logs = MashLog.objects.filter(batch__id=batch_id, id__gt=greaterthan_mashlog_id)
    else:
        logs = MashLog.objects.filter(batch__id=batch_id)

    if len(logs) > 0:
        last_mashlog = logs.latest('id')
        last_mashlog_id = last_mashlog.id
        # Load active mashing step
        try:
            active_mashing_step = MashLog.objects.filter(batch__id=batch_id).latest('id').active_mashing_step
        except MashLog.DoesNotExist:
            batch = Batch.objects.get(id=batch_id)
            active_mashing_step = batch.mashing_scheme.mashingstep_set.all()[0]
        active_mashing_step_index = last_mashlog.batch.mashing_scheme.mashingstep_set.filter(position__lt=active_mashing_step.position).count()
        active_mashing_step_state = last_mashlog.active_mashing_step_state
    else:
        last_mashlog_id = None
        active_mashing_step_index = 0
        active_mashing_step_state = 'A'



    data = {
        'chart': style_chart_data(logs),
        'latest_templog_id': last_mashlog_id,
        'active_mashing_step_index': active_mashing_step_index,
        'active_mashing_step_state': active_mashing_step_state
    }
    return simplejson.dumps({'status': 200, 'data': data})


def style_chart_data(mashing_temp_logs):
    result = []
    for mashing_temp_log in mashing_temp_logs:
        log = {
            'seconds': mashing_temp_log.get_seconds_offset(),
            'degrees': mashing_temp_log.degrees,
            'icon': mashing_temp_log.chart_icon,
            # 'state': mashing_temp_log.active_mashing_step_state,
            'heat': mashing_temp_log.heat,
            # 'step': mashing_temp_log.active_mashing_step.id
        }
        result.append(log)
    return result


@dajaxice_register
def delete_mashing_data(request, batch_id):

    MashLog.objects.filter(batch__id=batch_id).delete()
    return simplejson.dumps({'status': 200})