# -*- coding: utf-8 -*-
import time
from hashlib import md5
import datetime

from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.conf import settings

from core.views import JsonView
from .models import Ticket, Server
from videostore.models import Video


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class GetVideos(JsonView):
    def preprocess(self):
        srv = list(Server.objects.filter(
            is_enabled=True,
            ip_address=get_client_ip(self.request)
        ))
        if not srv:
            return {'error': 'Invalid server'}
        videos = Video.objects.filter(convert_status='converted')
        ret = []
        for v in videos:
            ret.append({'id': v.pk, 'title': v.title})
        return ret


class GetTicket(JsonView):

    def preprocess(self):
        srv = list(Server.objects.filter(
            is_enabled=True,
            ip_address=get_client_ip(self.request)
        ))
        if not srv:
            return {'error': 'Invalid server'}

        try:
            v = Video.objects.get(pk=self.kwargs.get('video_id'))
        except Video.DoesNotExist:
            return {'error': 'Video is not found'}

        if v.convert_status != 'converted' or not v.is_enabled:
            return {'error': 'Video unavailable'}

        hash = md5('%s%s' % (time.time(), settings.SECRET_KEY)).hexdigest()
        ticket = Ticket(
            video=v,
            hash=hash,
            client_id = get_client_ip(self.request)
        )
        ticket.save()

        return {
            'ticket': hash,
            'video': {
                'title': v.title,
                'thumb': str(v.thumb.url)
            }
        }


class ViewVideoByTicket(TemplateView):
    template_name = 'view_by_ticket.html'

    def get_context_data(self, **kwargs):

        hash_or_id = kwargs.get('ticket')
        if self.request.user.is_authenticated():
            video = get_object_or_404(Video, pk=hash_or_id)
        else:
            ticket = get_object_or_404(Ticket, hash=hash_or_id)
            if ticket.status != 'pending':
                raise Http404
            video = ticket.video

        return {'ticket': hash_or_id, "video": video}

def __ticket_valid(request, ticket):
    now = datetime.datetime.now()

    if ticket.status != 'seen':
        return False

    if ticket.client_id != get_client_ip(request):
        return False

    if (now-ticket.seen_at).total_seconds()>60*60:
        return False

    return True

def __base_stream(request, ticket, internal_stream_path):
    if not request.user.is_authenticated():
        ticket = get_object_or_404(Ticket, hash=ticket)

        if ticket.status == 'pending':
            ticket.status = 'seen'
            ticket.client_id = get_client_ip(request)
            ticket.seen_at = datetime.datetime.now()
            ticket.save()
        elif not __ticket_valid(request, ticket):
            raise Http404
        video = ticket.video
    else:
        video = get_object_or_404(Video, pk=ticket)

    response = HttpResponse(content_type='video/mp4')
    start = '?start=%s' % request.GET.get('start') if request.GET.get('start') else '?v=1'
    response["Content-Disposition"] = "attachment; filename=video_%s.flv" % video.pk
    response['X-Accel-Redirect'] = "/%s/%s%s" % (internal_stream_path, video.filename, start)
    return response

def stream_video(request, ticket):
    return __base_stream(request, ticket, 'protected')


def stream_mp4(request, ticket):
    return __base_stream(request, ticket, 'converted')

