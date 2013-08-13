# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from  django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import Category, ConvertingCommand, Video

class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    search_fields = ['title',]
admin.site.register(Category, CategoryAdmin)


class AdminVideoWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        html = super(AdminVideoWidget, self).render(name, value, attrs)
        if u'<a href' in html:
            parts = html.split('<br />')
            html = u'<p class="file-upload">'
            if value.instance.convert_status == 'converted':
                html += u'''
                    <a target="_blank" href="/video/%s/">Просмотр в новой вкладке</a><br />
                    Код вставки:<textarea style="width: 527px;" rows=1>&lt;iframe width="540" height="480" src="http://188.225.36.91/video/{TICKET_CODE}/"&gt;&lt;/iframe&gt;</textarea><br />
                ''' % value.instance.pk
            else:
                html += u'Видео %s еще не сконвертировано и пока его можно только заменить<br />' % value

            html = mark_safe(html+parts[1])
        return html

class VideoAdminForm(ModelForm):
    class Meta:
        model = Video
        widgets = {
            'video': AdminVideoWidget,
            'categories': CheckboxSelectMultiple
        }


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'convert_status', 'is_enabled')
    readonly_fields = ('convert_status','last_convert_msg')
    form = VideoAdminForm
    def save_model(self, request, obj, form, change):
        if 'video' in form.changed_data and change:
            obj.convert_status = 'pending'

        if not change:
            obj.user = request.user

        super(VideoAdmin, self).save_model(request, obj, form, change)


admin.site.register(Video, VideoAdmin)

class ConvertingCommandAdmin(admin.ModelAdmin):
    pass

admin.site.register(ConvertingCommand, ConvertingCommandAdmin)