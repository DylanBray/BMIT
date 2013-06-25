from django.db import models
from feincms.content.application import models as app_models
from django.utils.translation import ugettext_lazy as _

class contact( models.Model):
    day = models.DateField('day')
    name =  models.CharField(max_length=50)

    def __unicode__(self):
        return  u'%s %s' % (self.name, self.day)

    class Meta:
        unique_together = ('day', 'name')

class bl_booking(models.Model):
    beamline = models.CharField(max_length=50, choices =[('05B1-1', '05B1-1'), ('05ID-2', '05ID-2')])
    time_slot = models.CharField(max_length=25, choices=[('00:00-08:00', '00:00-08:00'), ('08:00-16:00', '08:00-16:00'),('16:00-24:00', '16:00-24:00')])
    user =  models.CharField(max_length=50)
    proposal =  models.CharField(max_length=50)
    date = models.DateField('day')

    class Meta:
        unique_together = ('date', 'time_slot', 'beamline')
        verbose_name = 'BeamLine Booking'

    def __unicode__(self):
        return u'%s %s' % (self.date, self.time_slot)

    @app_models.permalink
    def get_absolute_url(self):
        return ('index', 'bl_booking.urls', (), {
                'slug':  u'%s %s' % (self.date, self.time_slot)
                })

