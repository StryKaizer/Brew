from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Batch, MashLog
from brew.helpers import get_variable


def batchlisting(request):
    batches = Batch.objects.all().order_by('-number')

    return render_to_response('batchlisting.html', {'batches': batches}, context_instance=RequestContext(request))


def log(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    logs = MashLog.objects.filter(batch=batch)


    if logs.count() > 0:
        is_started = True
        first_log = logs[:1].get()

        last_log = logs.latest('id')
        seconds_running = last_log.created - first_log.created
        seconds_running = seconds_running.seconds
    else:
        is_started = False
        seconds_running = None

    if get_variable('mashing_batch_id_active', '0') == str(batch.id):
        is_running = True
    else:
        is_running = False

    return render_to_response('mashing.html',{
        'batch' : batch,
        'is_started': is_started,
        'is_running': is_running,
        'seconds_running': seconds_running
    }, context_instance=RequestContext(request))