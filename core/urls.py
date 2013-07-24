from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.contrib import admin
from ticketing.views import GetTicket, ViewVideoByTicket, stream_video
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^video/(?P<ticket>[0-9a-f]+)/$', ViewVideoByTicket.as_view(), name='video_by_ticket'),
    url(r'^stream/(?P<ticket>[0-9a-f]+)/$', stream_video, name='video_stream'),
    url(r'^get_ticket/(?P<video_id>[0-9a-f]+)/$', GetTicket.as_view(), name='get_ticket'),

    url(r'^', include(admin.site.urls)),
)

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static.static('/static/', document_root=settings.STATIC_ROOT)