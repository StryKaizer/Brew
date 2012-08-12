from django.db import models

class Brew(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class MashingSchemeItem(models.Model):
    brew = models.ForeignKey(Brew)
    minutes = models.CharField(max_length=3)
    degrees = models.CharField(max_length=3)

class BrewingDay(models.Model):
    brew = models.ForeignKey(Brew)
    brewing_date = models.DateTimeField('Brewing date')
    mashing_scheme_start = models.DateTimeField()
    def __unicode__(self):
        return str(self.brewing_date) + ' ' + str(self.brew)
    
class MashingTempLog(models.Model):
    brewing_day = models.ForeignKey(BrewingDay)
    degrees = models.CharField(max_length=3)    
    created = models.DateTimeField(auto_now_add=True)