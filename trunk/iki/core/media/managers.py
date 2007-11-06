# -*- encoding: utf-8 -*-
"""Default Media manager & related
"""
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

class MediaQuerySet(QuerySet):
    """Media default QuerySet"""
    def __init__(self, model=None):
        super(MediaQuerySet, self).__init__(model)

class MediaManager(models.Manager):
    """Media default Manager"""
    def __init__(self):
        super(MediaManager, self).__init__()

    def get_query_set(self):
        return MediaQuerySet(self.model)
