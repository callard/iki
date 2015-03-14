# How to store Metadata #

A _common_ problem is how to store metadata for our media files. Here is an attempt (and a discussion) about how to handle metadata for media file in the iki system.

Iki should support many media file, and as it is extensible it should handle any kind of metadata type. All metadata defined for a media file in iki should be stored in the file (if it's possible, indeed). In this way, the metadata are defined once for a file and is available anywhere the file is (because the metadata are **in** the file). Anyway, for a system like iki, 90% of data access are reading. To optimize these reading, we should store metadata in memory, and so in the database ; we also should sync the data with the file metadata but not so often ('cause file system access take much longer than database in memory access).

## Self-describing Metadata ##

Lots of metadata type, like XMP for example, are self-describing ; I mean, the element of the metadata are not static, you can create any element you want, and fill in whatever you want.

The problem is the following : most of the DBMS are _just_ relational and do not support the concept of object. How should we represent metadata object in database, when we don't even know each fields and which will be fill in or not ?

With a Object Database, or Object relational database it should be possible to have something dynamic. Any of the metadata object (in an object DBMS) could define their own field. But with a relational DBMS it's not possible at all.

## Current solution(s) ##

### Database storing ###

#### 1st solution ####
The solution we adopt, for the moment, is to store a _binay serialized_ object (python object) in a binary type of any Relationnal DBMS that support this kind of type. If the DBMS does not support binary type, we should store these _serialized object_ in a ascci (text) form.

The [Django](http://djangoproject.com) ORM does not support binary field for the moment (rev 6396) so we have to ~~hack django~~ create a custom field that support them. It's not really a good way of doing things, but, well, we don't have choices.

A quick and dirty implementation of a field that support _binary_ type in DBMS could be the following one.

```
#!python
from django.db.models import fields

class MetadataField(fields.Field):
    def __init__(self, **kwargs):
        super(MetadataField, self).__init__(**kwargs)

    def db_type(self):
        """Hack to tell django to use binary in place
        of other.. Watch for the backend too"""
        from django.db import get_creation_module
        creation_db = get_creation_module().__name__.split('.')
        if 'ado_mssql' in creation_db: return 'varbinary(%(maxlength)s)' % self.__dict__
        if 'sqlite3' in creation_db: return 'BLOB' % self.__dict__
        if 'postgresql_psycopg2' in creation_db or 'postgresql' in creation_db: return 'bytea' % self.__dict__
        if 'mysql' in creation_db: return 'varbinary(%(maxlength)s)' % self.__dict__

    def get_manipulator_field_objs(self):
        from django import oldforms
        return [oldforms.HiddenField]
```

In the end, we have a models **Metadata** that should look like the following one :

```
#!python
from django.db import models

class Metadata(models.Model):
    data = MetadataField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (("object_id", "content_type"),)

    # [..]
```

The MetadataField should _contain_ a serialized python object, using cPickle and binary serialization. It should be faster than using another way to serialize metadata (ie XML, JSON, or else) and we have that an object that is stored.

However, storing the Metadata object in an XML form (something like XMP) could be easier in the case of using another Language thant Python and when writing back metadata on the file.


#### 2nd solution ####

Another solution could be easily done with several table (and Django objects). I think about it when watching how are done the [DHIS 2.0](http://www.dhis.info) table schema.

The idea is to have 2 table : the first that store the type of metadata, with several information (name, type, namespace, etc..), and the second that associate a value and a related object (a media object indeed) with a metadata type.

With django, we could have the two following object :

```
#!python
from django.db import models

class Metadata(models.Model):
    type = models.ForeignKey('MetaType')
    value = models.XXXX # Here is the problem :D
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (("object_id", "content_type"),)

    # [..]

class MetaType(models.Model):
   name = models.CharField() # name of the type
   type = models.CharField() # type (programing) of it (Integer, field, tuple, ..)
   namespace = models.CharField() # the namespace (xmp:, exif:..)
   # anything else ?
```

### Metaobject, representation of metadata ###

MetaObject is the class that should represent a Metadata object, _for **any** type of ~~media~~ object_. We have to _support_ a notion of **namespace**, because some metadata format, like XMP, did it. Retrieving any field should be simple, but the field are _totally_ dynamic. An example should be easier to understand than a overfull explaination ; let's imagine that, in the following example, m is a MetaObject of a image (photo).

```
#!python

>>> m.exif.Orientation # 1: Horizontal
1
>>> m.exif.Software
"f-spot"
>>> m.dc.Creator #dc: Dublin Core
"Vincent Demeester"
>>> m.iptcCore.CountryCode
"fr"
>>> m.xmpRights.Owner
"Vincent Demeester"
>>> m.customNS.customField
"Custom field of a custom namespace"
>>> m.customNS
{'customField': 'customContent', 'customNumber': 12}

>>> m['xmpRights']['Owner']
"Vincent Demeester"

```

Everything can be _write back_ with XMP in the image file. This allow to have any custom namespace and so a really, huge, extensible way to write metadata for your media files. Now, let's see an example of a sound file.

```
#!python

>>> m.author
"Genesis"
>>> m.title
"Jesus He Knows Me"
>>> m.album
"Platinium Collection CD1"
>>> m.album_detail.year # album year
1996
>>> m.album_detail
{ 'year': 1996 }
>>> m.year # song year
1984

```

It simple to add any type of metadata too. However, some sound format does not support XMP or XML-like metadata format ; it'll be a problem de store _custom_ metadata in such files, but it's a question of distributing metadata, that's not our business for the moment.