# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, ConvertingCommand, Video

class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    search_fields = ['title',]
admin.site.register(Category, CategoryAdmin)


class VideoAdmin(admin.ModelAdmin):
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