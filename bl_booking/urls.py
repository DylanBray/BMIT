from django.conf.urls import patterns, url, include

from bl_booking import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', views.week, name='week'),
)
