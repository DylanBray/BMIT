from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.contrib import tagging
from gallery.models import GalleryContent
from news.models import news
from news.models import newsList

tagging.tag_model(Page)
#tagging.TagSelectField(Page)


Page.register_extensions(
    'feincms.module.extensions.datepublisher',   
    'feincms.module.extensions.seo', 
    'feincms.module.page.extensions.navigation',
    ) # Example set of extensions

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited')
        ),
    },{
        'title': _('Site map'),
        'path': 'sitemap.html',
        'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
        },{
        'title': _('2 Column Layout'),
        'path': '2column.html',
        'regions': (
            ('column1', _('Column 1')),
            ('column2', _('Column 2')),
            ('sidebar', _('Sidebar'), 'inherited'),
        ),
        },{
        'title': _('Home Layout'),
        'path': 'home.html',
        'regions': (
            ('column1', _('Column 1')),
            ('column2', _('Column 2')),
            ('column3', _('Column 3')),
            ('column4', _('Column 4')),
            ('status1', _('Status 1')),
            ('status2', _('Status 2')),
        ),
        })


Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('plainImage', _('plainImage')),
    ))
Page.create_content_type(GalleryContent)


Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('bl_booking.urls', 'Schedule'),
    ('aurora.urls', 'Aurora Schedule'),
    ('news.urls', 'News'),
    ))

Page.create_content_type(newsList)



