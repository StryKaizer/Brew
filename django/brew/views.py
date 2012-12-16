from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def batchlisting(request):
    
    
    
    return render_to_response('batchlisting.html',{}, context_instance=RequestContext(request))


def log(request, mash_id):
  
    
    return render_to_response('mashing.html',{}, context_instance=RequestContext(request))