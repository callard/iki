# -*- encoding: utf-8 -*-
"""Photo contrib application :  models
"""
import datetime
import random

from django.db import models
from django.contrib.auth.models import User

# i18n
from django.utils.translation import gettext_lazy as _
# magic iki stuff ;)
from iki.core.media import Media

class Album(models.Model):
    name = models.CharField(_("name"), maxlength=25, db_index=True,
                            help_text=_('Name of your album'))
    slug = models.SlugField(_("slug"), prepopulate_from=['name'],
                            help_text=_('Automatically built from the name'),)
    desc = models.TextField(_("description"), db_index=True,
                            help_text=_('Description'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_("Owner"))

    class Meta:
        unique_together=(('name', 'owner'),)

    class Admin:
        list_display = ('name', 'owner',)
        list_filter = ('owner',)
        search_fields = ('name', 'desc',)
        ordering = ('name',)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name

    def save(self):
        super(Album, self).save()

    def get_absolute_url(self):
        raise NotImplementedError

class Photo(Media):
    """Photo model for iki
    You just have to define here the non-common field (the others are
    define elsewhere, in Media)

    >>> p1 = Photo()
    """
    album = models.ForeignKey(Album, verbose_name=_("Album"), null=True,
                              blank=True)
    
    
