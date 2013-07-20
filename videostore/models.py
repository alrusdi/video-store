# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


CONVERTING_COMMAND_MATCH_CHOICES = (
    ('extention', _('Extension')),
    ('meta', _('Meta info')),
    ('name', _('File name')),
)

class ConvertingCommand(models.Model):
    '''
    System commands for convertion videos to desired format
    '''
    match_by = models.CharField(
        max_length=50,
        verbose_name=_('Match by'),
        choices=CONVERTING_COMMAND_MATCH_CHOICES,
        help_text=_('Video param to detected from if this command should be used to convert given video'),
    )
    match_regex = models.CharField(
        max_length=200,
        verbose_name=_('RegExp to match video file'),
    )
    is_enabled = models.BooleanField(
        verbose_name=_('Enabled?'),
        default=True,
    )
    command = models.TextField(
        verbose_name=_('System command to convert video'),
        help_text = 'Example: /usr/bin/avconv -y -i %(input_file)s -acodec libmp3lame -ar 44100 -f flv %(output_file)s',
    )
    sort_pos = models.PositiveIntegerField(
        verbose_name=_('Order'),
        help_text=_('If more than one command matched to convert given video - topmost by Order will be used'),
        default=0,
    )

    def __unicode__(self):
        return u'%s "%s..."' % (self.sort_pos, self.command[0:50])

    def save(self, **kwargs):
        if not self.sort_pos:
            self.sort_pos = (self.__class__.objects.all().aggregate(models.Max('id')).get('id__max') or 1)*10

        return super(ConvertingCommand, self).save(**kwargs)

    class Meta:
        verbose_name = _(u'Video convert command')
        verbose_name_plural = _(u'Video convert commands')

class Category(MPTTModel):
    '''
    Category of video to easy search/classify videos
    '''
    parent = TreeForeignKey(
        'self',
        verbose_name = _(u'Parent category'),
        related_name = 'children',
        blank = True, null = True,
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Title'),
    )

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')


VIDEO_CONVERSION_STATUS_CHOICES = (
    ('pending', _('Pending convert')),
    ('started', _('Convert started')),
    ('converted', _('Converted')),
    ('error', _('Not converted due to error')),
)


class Video(models.Model):
    '''
    Uploaded video
    '''
    categories = TreeManyToManyField(
        Category,
        verbose_name=_(u'Categories')
    )

    title = models.CharField(
        max_length=500,
        verbose_name=_('Title'),
    )

    video = models.FileField(
        verbose_name=_('Video file'),
        upload_to='videos',
    )

    thumb = models.ImageField(
        verbose_name=_('Thumbnail image'),
        upload_to='thumbs',
    )

    description = models.TextField(
        verbose_name=_('Description'),
        null=True, blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created time'),
        auto_now_add=True,
    )

    convert_status = models.CharField(
        max_length=50,
        verbose_name=_('Video conversion status'),
        choices=VIDEO_CONVERSION_STATUS_CHOICES,
        default='pending',
    )

    converted_at = models.DateTimeField(
        verbose_name=_('Convert time'),
        editable=False, null=True, blank=True,
    )

    last_convert_msg = models.TextField(
        verbose_name=_('Message from last converting command'),
        editable=False,
    )

    user = models.ForeignKey(
        User,
        verbose_name=_('Uploaded by'),
        editable=False,
    )

    is_enabled = models.BooleanField(
        verbose_name=_('Video enabled for view?'),
        default=True,
    )

    meta_info = models.TextField(
        verbose_name=_('Meta info about original video'),
        null=True,
        editable=False,
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
