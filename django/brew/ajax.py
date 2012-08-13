from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from brew.tasks import init_mashing




@dajaxice_register
def start_mashing(request):
    init_mashing.delay()
    return simplejson.dumps({'status':200})


@dajaxice_register
def stop_mashing(request):
    return simplejson.dumps({'status':200})

