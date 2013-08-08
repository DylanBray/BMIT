from django.db import models
from tinymce.models import HTMLField
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.content.application import models as app_models
class news(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    content = HTMLField()

    class Meta:
        unique_together = ("date", "title")
        verbose_name = "News Article"
        

    def __unicode__(self):
        return  u'%s %s' % (self.title, self.date)
   
    @app_models.permalink
    def get_absolute_url(self):
        return ('index', 'news.urls', (), {})


class newsList(models.Model):
    number = models.IntegerField()

    class Meta:
        abstract = True

    def get_queryset_for_render(self):
        return news.objects.all()

    def render(self, **kwargs):
        context = {
            'object_list': self.get_queryset_for_render()[:self.number],
            'request': kwargs.get('request'),
        }
        return render_to_string('news/list.html', context)
