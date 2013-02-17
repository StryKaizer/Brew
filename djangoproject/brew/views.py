from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Batch

def batchlisting(request):
    
    batches = Batch.objects.all()

    return render_to_response('batchlisting.html', {'batches': batches}, context_instance=RequestContext(request))


def log(request, batch_id):
    batch = Batch.objects.get(id=batch_id)

    return render_to_response('mashing.html',{'batch' : batch}, context_instance=RequestContext(request))