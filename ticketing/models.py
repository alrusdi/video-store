# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from videostore.models import Video

TICKET_STATUS_CHOICES = (
    ('pending', _('Pending view')),
    ('seen', _('Seen')),
    ('overdue', _('Overdue')),
    ('blocked', _('Blocked')),
)


class Ticket(models.Model):

    video = models.ForeignKey(
        Video,
        verbose_name=_('Video')
    )

    hash = models.CharField(
        max_length=50,
        editable = False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created time'),
        auto_now_add=True,
    )

    seen_at = models.DateTimeField(
        verbose_name=_('Created time'),
        null=True,
    )

    valid_to = models.DateTimeField(
        verbose_name=_('Valid to'),
        null=True,
    )

    status = models.CharField(
        max_length=50,
        choices=TICKET_STATUS_CHOICES,
        default='pending',
    )

    headers = models.TextField(
        verbose_name=_('Dump of viewer HTTP headers'),
        editable=False
    )

    def __unicode__(self):
        return u'#%s %s %s' % (self.id, self.created_at, self.status)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
