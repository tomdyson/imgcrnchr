from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<crunch_factor>[0-9]+)?/?(?P<image_url>.+)$', 'core.views.crunch', {}, name="crunch"),
)
