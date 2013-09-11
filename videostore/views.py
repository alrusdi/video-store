# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageEnhance
from django.conf import settings
from django.http import HttpResponse


def watermark(request, file):
    fname = os.path.basename(file)
    res_path = os.path.join(settings.MEDIA_ROOT, 'wmthumbs', fname)

    if not os.path.exists(res_path):
        mark = Image.open(os.path.join(settings.ROOT_PATH, 'static', 'images', 'play.png'))
        im = Image.open(os.path.join(settings.MEDIA_ROOT, 'thumbs', fname))

        ratio = float(mark.size[0]) / float(mark.size[1])
        w = float(im.size[0]) / 100.0 * 30
        h = int(w / ratio)
        mark = mark.resize((int(w), h), Image.ANTIALIAS)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        layer = Image.new('RGBA', im.size, (0,0,0,0))
        position = (im.size[0] / 2 - mark.size[0] / 2, im.size[1] / 2 - mark.size[1] / 2)
        layer.paste(mark, position)

        Image.composite(layer, im, layer).save(res_path)

    response = HttpResponse()
    response['X-Sendfile'] = res_path
    response['Content-Type'] = ''

    return response

