from brew.models import Variable


def set_variable(key, value):
    variable, created = Variable.objects.get_or_create(key=key)
    variable.value = value
    variable.save()

def get_variable(key, default_value=None):
    variable, created = Variable.objects.get_or_create(key=key)
    if created:
        return default_value
    return variable.value