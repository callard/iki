
# -*- encoding: utf-8 -*-
"""Default Media fields & related
"""
from django.db.models.fields import FileField
from django.db.models import signals
from django.dispatch import dispatcher

class MediaField(FileField):
    """MediaField: a special FileField for iki
    """
    def __init__(self, **kwargs):
        kwargs['blank'] = kwargs.get('blank', True)
        #kwargs['validator_list'] = [isTagList] + kwargs.get('validator_list', [])
        super(MediaField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        super(MediaField, self).contribute_to_class(cls, name)

        # Make this object the descriptor for field access.
        setattr(cls, self.name, self)

    def get_internal_type(self):
        return 'FileField'
