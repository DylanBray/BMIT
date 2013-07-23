from django.conf.urls import patterns, include, url
from feincms.module.page.sitemap import PageSitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bmit.views.home', name='home'),
    # url(r'^beamline-schedule/', include('cms.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
            
     url(r'^gallery/', include('gallery.urls')),
     (r'^tinymce/', include('tinymce.urls')),
     
)

from feincms.module.page.sitemap import PageSitemap
sitemaps = {'pages' : PageSitemap}

urlpatterns += patterns('',
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    )


urlpatterns += patterns('',

     url(r'', include('feincms.urls')),

)

