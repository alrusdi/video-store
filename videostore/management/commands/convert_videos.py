# -*- coding: utf-8 -*-
import re
import os
import commands
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from videostore.models import Video, ConvertingCommand


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'Converts oldest unconverted video'


    def handle(self, *args, **options):
        # Choosing oldest unconverted video

        video = Video.objects.filter(is_enabled=True,convert_status='pending').order_by('-pk')
        if not video:
            print 'No video found bypassing call...'
            return
        video = video[0]
        video.convert_status = 'started'
        video.save()


        file_path = '/'.join(str(video.video.file).split('/')[0:-1])
        full_name = str(video.video.file).split('/')[-1]
        parts = full_name.split('.')

        video_info = {
            'name': '.'.join(parts[0:-1]),
            'extension': parts[-1],
            'meta': '' # commands.getoutput('/usr/bin/avprobe "%s"' % str(video.video.file)))
        }
        cmds = ConvertingCommand.objects.filter(is_enabled=True).order_by('sort_pos')
        cmd = None
        for c in cmds:
            if re.match(c.match_regex, video_info.get(c.match_by)):
                cmd = c
                break


        if not cmd:
            video.convert_status = 'error'
            video.last_convert_msg = u'Conversion command not found'
            video.save()
            return


        try:
            params = {
                'input_file': str(video.video.file),
                'output_file': video.converted_path
            }
            output = commands.getoutput(cmd.command % params)
        except:
            video.convert_status = 'error'
            video.last_convert_msg = u'Exception while converting'
            video.save()
            raise

        video.convert_status = 'converted'
        video.last_convert_msg = output
        video.converted_at = datetime.datetime.now()
        video.save()
        print 'Video converted'

