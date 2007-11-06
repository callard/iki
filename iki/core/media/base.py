# -*- encoding: utf-8 -*-
"""iki.core.media : Common methods for iki/django models

These class are class that media models should inherit, in order to work in
the iki media manager application.
"""
import random

from django.db.models.base import Model, ModelBase
from django.db.models.fields import *
from django.db.models.fields.related import ForeignKey

# django.contrib
from django.contrib.auth.models import User
# i18n
from django.utils.translation import gettext_lazy as _
# tagging
from tagging.fields import TagField

class MediaBase(ModelBase):
    """Metaclass for all media models. Inherit from the metaclasse for
    all django models (because, there no other choice)
    """    
    def __new__(cls, name, bases, attrs):
        # If this isn't a subclass of Media, don't do anything special
        try:
            if not filter(lambda b: issubclass(b, Media), bases):
                return super(MediaBase, cls).__new__(cls, name, bases, attrs)
        except NameError:
            # 'Media' isn't defined yet, meaning we're looking at Media class,
            # defined below
            new_class = super(MediaBase, cls).__new__(cls, name, bases, attrs)
            new_class.add_field('media')
            #new_class.add_field('original')
            return new_class
        
        new_class = ModelBase.__new__(cls, name, bases, attrs)

        # try to load a custom manager
        try:
            manager_import = new_class.__module__.split('.')
            manager_import.pop()
            manager_import.append('managers')
            managers = __import__(".".join(manager_import), globals(), locals(),
                                  ['%sMediaManager' % new_class.__name__], -1)
            manager = getattr(managers,
                                  "%sMediaManager" % new_class.__name__)
            manager().contribute_to_class(new_class, 'objects')
            manager().contribute_to_class(new_class, '_default_manager')
        except:
            from iki.core.media.managers import MediaManager
            MediaManager().contribute_to_class(new_class, 'objects')
            MediaManager().contribute_to_class(new_class, '_default_manager')

        new_class.add_field('media')
        #new_class.add_field('original')

        # finaly, let's go
        return new_class

    def get_media(cls):
        """Trying to load a custom MediaFIeld"""
        lname = cls.__name__.lower()
        try:
            field_import = cls.__module__.split('.')
            field_import.pop()
            field_import.append('fields')
            fields = __import__(".".join(field_import), globals(), locals(),
                                ['%sMediaField' % cls.__name__], -1)
            field = getattr(fields, '%sMediaField' % cls.__name__)(upload_to="%s/tmp/%s-%s-%s" % (
                    lname, "%Y%m%d%H", "%I%S", random.randint(1, 10000)))
        except:
            from iki.core.media.fields import MediaField
            field = MediaField(upload_to="%s/tmp/%s-%s-%s" % (lname, "%Y%m%d%H",
                                                              "%I%S", random.randint(1, 10000)))
        return field

    def get_original(cls):
        field = ForeignKey(cls, related_name="from", null=True, blank=True)
        return field

    def add_field(cls, name):
        added = False
        field = getattr(cls, 'get_%s' % name)()
        
        for f in cls._meta.fields:
            if f.name == name:
                cls._meta.fields.remove(f)
                field.contribute_to_class(cls, name)
                added = True
                break

        if not added:
            field.contribute_to_class(cls, name)

class Media(Model):
    __metaclass__ = MediaBase

    name = CharField(_('name'), maxlength=25, db_index=True,
                       help_text=_('Name'))
    description = TextField(_('description'), db_index=True,
                            help_text=_('Description of the media'),
                            blank=True)
    # media field defined by the __metaclass__
    tags = TagField(blank=True)
    private = BooleanField(default=False,
                           help_text=_('Is this photo private ?'))
    adult = BooleanField(default=False,
                         help_text=_('Is it an adult content ?'))
    # original field (foreignkey) is defined by the __metaclass__
    owner = ForeignKey(User, verbose_name=_("Owner"))

    class Meta:
        pass

    class Admin:
        search_fields = ('name', 'description', 'tags', 'owner__username',)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name

    def save(self, ip_address=None):
        self.ip_address = ip_address
        if not ip_address:
            self.ip_address = '0.0.0.0'
        super(Media, self).save()

    def get_absolute_url(self):
        raise NotImplementedError

    def delete(self):
        # Do your stuff here
        super(Media, self).delete(self)

    def __move_media(self, destination):
        """Move the media to destination"""
        raise NotImplementedError

    def __copy_media(self, destination):
        """Copy the media to destination"""
        raise NotImplementedError

    def __delete_media(self):
        """Delete media (from fs)"""
        raise NotImplementedError

    def get_thumbnail(self, size):
        """Get the thumbnail"""
        raise NotImplementedError
