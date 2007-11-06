# -*- encoding: utf-8 -*-
"""Metadata models
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class MetaType(models.Model):
    """Type of metadata, name, and namespace

    example : xmp.Copyright :: String
    """
    name = models.CharField(maxlength=100)
    type = models.CharField(maxlength=100)
    namespace = models.CharField(maxlength=100)

    class Meta:
        pass

    class Admin:
        pass

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name

    def save(self):
        super(MetaType, self).save()

    def get_absolute_url(self):
        return ''

class Metadata(models.Model):
    """Metadata
    """
    type = models.ForeignKey(MetaType)
    value = models.CharField(maxlength=300)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (("object_id", "content_type"),)

    class Admin:
        pass

    def __unicode__(self):
        return u"%s:%s:%s" % (object, type, value)

    def __str__(self):
        return "%s:%s:%s" % (object, type, value)

    def save(self):
        super(Metadata, self).save()

    def get_absolute_url(self):
        return ''

