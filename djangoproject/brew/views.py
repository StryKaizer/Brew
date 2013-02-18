from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Batch, MashingTempLog

def batchlisting(request):
    
    batches = Batch.objects.all()

    return render_to_response('batchlisting.html', {'batches': batches}, context_instance=RequestContext(request))


def log(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    if len(MashingTempLog.objects.filter(batch=batch)) > 0:
        is_started = True
    else:
        is_started = False

    return render_to_response('mashing.html',{'batch' : batch, 'is_started': is_started}, context_instance=RequestContext(request))