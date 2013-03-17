from django.db import models
import time
from datetime import datetime
import pytz

CHART_ICONS = (
    ('start1', 'Start Step 1'), ('stop1', 'Finished Step 1'),
    ('start2', 'Start Step 2'), ('stop2', 'Finished Step 2'),
    ('start3', 'Start Step 3'), ('stop3', 'Finished Step 3'),
    ('start4', 'Start Step 4'), ('stop4', 'Finished Step 4'),
    ('start5', 'Start Step 5'), ('stop5', 'Finished Step 5'),
    ('start6', 'Start Step 6'), ('stop6', 'Finished Step 6'),
    ('start7', 'Start Step 7'), ('stop7', 'Finished Step 7'),
    ('start8', 'Start Step 8'), ('stop8', 'Finished Step 8'),
    ('start9', 'Start Step 9'), ('stop9', 'Finished Step 9'),
    ('start10', 'Start Step 10'), ('stop10', 'Finished Step 10'),
    ('finished', 'Finished'),
)

MASHINGSTEP_STATES = (
    ('approach', 'Approach'),
    ('stay', 'Stay'),
    ('finished', 'Finished'),
)

MASHINGSTEP_APPROACH_DIRECTIONS = (
    ('tbd', 'To be defined'),
    ('heat', 'Heat'),
    ('cool', 'Cool'),
)

# The model MashingScheme
class MashingScheme(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


# The model MashingStep is used to hold data for one step in a MashingScheme.
class MashingStep(models.Model):
    position = models.PositiveSmallIntegerField("Position")
    mashing_scheme = models.ForeignKey(MashingScheme)
    minutes = models.CharField(max_length=3)
    degrees = models.CharField(max_length=3)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return str(self.minutes) + ' min -  ' + str(self.degrees) + ' degrees'


# The model Batch is used to define a brewing day, which will hold logs etc.
class Batch(models.Model):
    mashing_scheme = models.ForeignKey(MashingScheme)
    number = models.IntegerField(max_length=3)
    brewing_date = models.DateTimeField('Brewing date')

    # Data storage for mashing proces
    mashing_process_is_running = models.BooleanField()
    active_mashingstep = models.ForeignKey(MashingStep)
    active_mashingstep_state = models.CharField(max_length=10, choices=MASHINGSTEP_STATES, default='approach')
    active_mashingstep_state_start = models.DateTimeField()
    active_mashingstep_approach_direction = models.CharField(max_length=10, choices=MASHINGSTEP_APPROACH_DIRECTIONS, default='tbd')
    heat = models.BooleanField()
    cool = models.BooleanField()

    def __unicode__(self):
        return str(self.number)

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Batch.objects.get(pk=self.pk)

            # If state changes, update active_mashingstep_state_start to current timestamp
            if orig.active_mashingstep_state != self.active_mashingstep_state:
                self.active_mashingstep_state_start = datetime.now(pytz.utc)
        super(Batch, self).save(*args, **kw)


# The model MashLog is used to hold data of 1 measure for a certain Batch.
class MashLog(models.Model):
    batch = models.ForeignKey(Batch)
    degrees = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    active_mashing_step = models.ForeignKey(MashingStep)
    active_mashing_step_state = models.CharField(max_length=10, choices=MASHINGSTEP_STATES)
    chart_icon = models.CharField(max_length=30, choices=CHART_ICONS, blank=True, null=True)
    heat = models.BooleanField()

    def get_seconds_offset(self):
        first_log = MashLog.objects.filter(batch=self.batch)[:1].get()
        return int(time.mktime(self.created.timetuple()) - time.mktime(first_log.created.timetuple()))

    def __unicode__(self):
        return str(self.id) + ' - ' + str(self.created) +' ' +  str(self.active_mashing_step) + ' ' + str(self.active_mashing_step_state)


# The model Variable is used for a simple key-value store functionality.
class Variable(models.Model):
    key = models.CharField(max_length=127)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.key) + ' - ' + str(self.value)