
"""History module, mostly stolen from AuditTrail :
http://code.djangoproject.com/wiki/AuditTrail
"""
import re

from django.dispatch import dispatcher
from django.db import models
from django.core.exceptions import ImproperlyConfigured

value_error_re = re.compile("^.+'(.+)'$")

class History(object):
    """Store history changes on other applications, with dynamic model
    generation
    """
    def __init__(self, show_in_admin=False):
        self.show_in_admin = show_in_admin

    def contribute_to_class(self, cls, name):
        # This should only get added once the class is otherwise complete

        def _contribute(sender):
            model = create_history_model(sender, self.show_in_admin)
            descriptor = HistoryDescriptor(model.objects,
                                           sender._meta.pk.attname)
            setattr(sender, name, descriptor)

            def _history(sender, instance):
                # Write model changes to the audit model
                kwargs = {}
                for field in sender._meta.fields:
                    kwargs[field.attname] = getattr(instance, field.attname)
                kwargs['_history_ip'] = instance.ip_address
                model.objects.create(**kwargs)
            dispatcher.connect(_history, signal=models.signals.post_save,
                               sender=cls, weak=False)

        dispatcher.connect(_contribute, signal=models.signals.class_prepared,
                           sender=cls, weak=False)

class HistoryDescriptor(object):
    def __init__(self, manager, pk_attribute):
        self.manager = manager
        self.pk_attribute = pk_attribute

    def __get__(self, instance=None, owner=None):
        if instance == None:
            raise AttributeError, "History is only accessible via %s instances." % type.__name__
        return create_history_manager(self.manager, self.pk_attribute, instance._get_pk_val())

    def __set__(self, instance, value):
        raise AttributeError, "History may not be edited in this manner."

def create_history_manager(manager, pk_attribute, pk):
    """Create an history manager based on the current object"""
    class HistoryManager(manager.__class__):
        def __init__(self):
            self.model = manager.model

        def get_query_set(self):
            return super(HistoryManager, self).get_query_set().filter(**{pk_attribute: pk})
    return HistoryManager()

def create_history_model(cls, show_in_admin):
    """Create an audit model for the specific class"""
    name = cls.__name__ + 'History'

    class Meta:
        db_table = '%s_history' % cls._meta.db_table
        verbose_name_plural = '%s history' % cls._meta.verbose_name
        ordering = ['-_history_timestamp']

    # Set up a dictionary to simulate declarations within a class
    attrs = {
        '__module__': cls.__module__,
        'Meta': Meta,
        '_history_id': models.AutoField(primary_key=True),
        '_history_timestamp': models.DateTimeField(auto_now_add=True),
        '_history_ip': models.IPAddressField(blank=True, null=True),
        '_history__str__': cls.__str__.im_func,
        '__str__': lambda self: '%s as of %s' % (self._history__str__(),
                                                 self._history_timestamp),
        #'objects': HistoryManager(), # not really needed for the moment
        }

    if show_in_admin:
        # Enable admin integration
        class Admin:
            pass
        attrs['Admin'] = Admin

    # Copy the fields from the existing model to the audit model
    for field in cls._meta.fields:
        if field.attname in attrs:
            raise ImproperlyConfigured, "%s cannot use %s as it is needed by History." % (cls.__name__, field.attname)
        attrs[field.attname] = copy_field(field)

    return type(name, (models.Model,), attrs)

def copy_field(field):
    """Copy an instantiated field to a new instantiated field"""
    if isinstance(field, models.AutoField) or isinstance(field, models.ForeignKey):
        # History models have a separate AutoField
        return models.IntegerField(db_index=True, editable=False,
                                   null=field.null, blank=field.blank)

    copied_field = None
    cls = field.__class__

    # Use the field's attributes to start with
    kwargs = field.__dict__.copy()

    # Swap primary keys for ordinary indexes
    if field.primary_key:
        kwargs['db_index'] = True
        del kwargs['primary_key']

    # Some hackery to copy the field
    while copied_field is None:
        try:
            copied_field = cls(**kwargs)
        except (TypeError, ValueError), e:
            # Some attributes, like creation_counter, aren't valid arguments
            # So try to remove that argument so the field can try again
            try:
                del kwargs[value_error_re.match(str(e)).group(1)]
            except:
                # The attribute was already removed, and something's still going wrong
                raise e

    return copied_field
