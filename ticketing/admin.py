# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Ticket, Server


# class TicketAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(Ticket, TicketAdmin)


class ServerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Server, ServerAdmin)