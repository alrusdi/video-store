# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib import admin
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
                    Код вставки:<textarea style="width: 527px;" rows=1>&lt;iframe width="540" height="480" src="http://188.225.36.91/video/%s/"&gt;&lt;/iframe&gt;</textarea><br />
                    %s
                ''' % (value.instance.pk, value.instance.pk, parts[1])
            html = mark_safe(html)

        return html

class VideoAdminForm(ModelForm):
    class Meta:
        model = Video
        widgets = {
            'video': AdminVideoWidget,
        }


class VideoAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)
    readonly_fields = ('convert_status',)
    form = VideoAdminForm
    def save_model(self, request, obj, form, change):
        if 'video' in form.changed_data and change:
            obj.status = 'pending'

        if not change:
            obj.user = request.user

        super(VideoAdmin, self).save_model(request, obj, form, change)


admin.site.register(Video, VideoAdmin)

class ConvertingCommandAdmin(admin.ModelAdmin):
    pass

admin.site.register(ConvertingCommand, ConvertingCommandAdmin)