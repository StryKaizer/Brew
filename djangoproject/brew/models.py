from django.db import models
import time

# The model Brew is used to define the Beer name.  A Brew can be made multiple times.
class Brew(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

# The model MashingSchemeItem is used to set 1 line in a MashingScheme for a certain Brew.
class MashingSchemeItem(models.Model):
    brew = models.ForeignKey(Brew)
    minutes = models.CharField(max_length=3)
    degrees = models.CharField(max_length=3)

# The model Batch is used to define a brewing day, which will hold logs etc.
class Batch(models.Model):
    brew = models.ForeignKey(Brew)
    number = models.IntegerField(max_length=3)
    brewing_date = models.DateTimeField('Brewing date')
    mashing_scheme_start = models.DateTimeField()
    def __unicode__(self):
        return str(self.brewing_date) + ' ' + str(self.brew)
   
# The model MashingTempLog is used to hold data of 1 measure for a certain Batch.
class MashingTempLog(models.Model):
    batch = models.ForeignKey(Batch)
    degrees = models.CharField(max_length=3)    
    created = models.DateTimeField(auto_now_add=True)
    def get_seconds_offset(self):
        first_log = MashingTempLog.objects.filter(batch=self.batch)[:1].get()
        return int(time.mktime(self.created.timetuple()) - time.mktime(first_log.created.timetuple()))
    def __unicode__(self):
        return str(self.id) + ' - ' + str(self.created)

# The model Variable is used for a simple key-value store functionality.
class Variable(models.Model):
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=255)
    def __unicode__(self):
        return str(self.key) + ' - ' + str(self.value)