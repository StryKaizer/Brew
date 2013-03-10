from django.db import models
import time

MASHINGSTEP_STATES = (
    ('H', 'Heat'),
    ('C', 'Cool'),
    ('S', 'Stay'),
    ('F', 'Finished'),
)


# The model MashingScheme
class MashingScheme(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


# The model MashingStep is used to hold data for one step in a MashingScheme.
class MashingStep(models.Model):
    mashing_scheme = models.ForeignKey(MashingScheme)
    minutes = models.CharField(max_length=3)
    degrees = models.CharField(max_length=3)

    def __unicode__(self):
        return str(self.minutes) + ' min -  ' + str(self.degrees) + ' degrees'


# The model Batch is used to define a brewing day, which will hold logs etc.
class Batch(models.Model):
    mashing_scheme = models.ForeignKey(MashingScheme)
    number = models.IntegerField(max_length=3)
    brewing_date = models.DateTimeField('Brewing date')

    def __unicode__(self):
        return str(self.brewing_date) + ' ' + str(self.number)


# The model MashLog is used to hold data of 1 measure for a certain Batch.
class MashLog(models.Model):
    batch = models.ForeignKey(Batch)
    degrees = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    active_mashing_step = models.ForeignKey(MashingStep)
    active_mashing_step_state = models.CharField(max_length=1, choices=MASHINGSTEP_STATES)

    def get_seconds_offset(self):
        first_log = MashLog.objects.filter(batch=self.batch)[:1].get()
        return int(time.mktime(self.created.timetuple()) - time.mktime(first_log.created.timetuple()))

    def __unicode__(self):
        return str(self.id) + ' - ' + str(self.created)


# The model Variable is used for a simple key-value store functionality.
class Variable(models.Model):
    key = models.CharField(max_length=127)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.key) + ' - ' + str(self.value)