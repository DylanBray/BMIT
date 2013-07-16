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
