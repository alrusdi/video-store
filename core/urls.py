from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.contrib import admin
from ticketing.views import GetTicket, GetVideos, ViewVideoByTicket, stream_video, stream_mp4
from videostore.views import watermark
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/wmthumbs/(?P<file>.*)$', watermark, name='make_watermark'),
    url(r'^video/(?P<ticket>[0-9a-f]+)/$', ViewVideoByTicket.as_view(), name='video_by_ticket'),
    url(r'^stream/(?P<ticket>[0-9a-f]+)/$', stream_video, name='video_stream'),
    url(r'^streammp4/(?P<ticket>[0-9a-f]+)/$', stream_mp4, name='video_streammp4'),
    url(r'^get_ticket/(?P<video_id>[0-9]+)/$', GetTicket.as_view(), name='get_ticket'),
    url(r'^get_videos/$', GetVideos.as_view(), name='get_videos'),
    url(r'^', include(admin.site.urls)),
)

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static.static('/static/', document_root=settings.STATIC_ROOT)
