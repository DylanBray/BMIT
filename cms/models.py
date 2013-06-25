from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.contrib import tagging

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
        'title': _('Site msp'),
        'path': 'sitemap.html',
        'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
        })


Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
    ))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('bl_booking.urls', 'Schedule'),
    ))

